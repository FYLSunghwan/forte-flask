import os
import mir_eval
import pretty_midi as pm
from utils import logger
from model import *
from utils.mir_eval_modules import audio_file_to_features, idx2chord, idx2voca_chord, get_audio_paths
import argparse
import warnings

class ChordDetector():
    def __init__(self, path, voca=False):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.config = HParams.load("run_config.yaml")

        if voca == True:
            self.config.feature['large_voca'] = True
            self.config.model['num_chords'] = 170
            self.model_file = './pretrained/btc_model_large_voca.pt'
            self.idx_to_chord = idx2voca_chord()
        else:
            self.model_file = './pretrained/btc_model.pt'
            self.idx_to_chord = idx2chord

        self.model = BTC_model(config=self.config.model).to(self.device)

        if os.path.isfile(self.model_file):
            self.checkpoint = torch.load(self.model_file)
            self.mean = self.checkpoint['mean']
            self.std = self.checkpoint['std']
            self.model.load_state_dict(self.checkpoint['model'])
        
        self.audio_path = path

    def run(self):
        # Load mp3
        feature, feature_per_second, song_length_second = audio_file_to_features(self.audio_path, self.config)
        logger.info("audio file loaded and feature computation success : %s" % self.audio_path)

        # Majmin type chord recognition
        feature = feature.T
        feature = (feature - self.mean) / self.std
        time_unit = feature_per_second
        n_timestep = self.config.model['timestep']

        num_pad = n_timestep - (feature.shape[0] % n_timestep)
        feature = np.pad(feature, ((0, num_pad), (0, 0)), mode="constant", constant_values=0)
        num_instance = feature.shape[0] // n_timestep

        start_time = 0.0
        lines = []
        with torch.no_grad():
            self.model.eval()
            feature = torch.tensor(feature, dtype=torch.float32).unsqueeze(0).to(self.device)
            for t in range(num_instance):
                self_attn_output, _ = self.model.self_attn_layers(feature[:, n_timestep * t:n_timestep * (t + 1), :])
                prediction, _ = self.model.output_layer(self_attn_output)
                prediction = prediction.squeeze()
                for i in range(n_timestep):
                    if t == 0 and i == 0:
                        prev_chord = prediction[i].item()
                        continue
                    if prediction[i].item() != prev_chord:
                        lines.append({
                            'start_time' : start_time,
                            'end_time' : time_unit * (n_timestep * t + i),
                            'chord_name' : self.idx_to_chord[prev_chord]
                        })
                        start_time = time_unit * (n_timestep * t + i)
                        prev_chord = prediction[i].item()
                    if t == num_instance - 1 and i + num_pad == n_timestep:
                        if start_time != time_unit * (n_timestep * t + i):
                            lines.append({
                                'start_time' : start_time,
                                'end_time' : time_unit * (n_timestep * t + i),
                                'chord_name' : self.idx_to_chord[prev_chord]
                            })
                        break

        return lines

if __name__ == '__main__':
    det = ChordDetector('welove.mp3')
    det.run()