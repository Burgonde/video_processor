import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess

class VideoProcessorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Video Processor")
        self.geometry("800x200")

        self.file_path = None
        self.frame_width = tk.StringVar(value="512")
        self.fps = tk.StringVar(value="10")
        self.start_timecode = tk.StringVar(value="00:00:00")
        self.end_timecode = tk.StringVar(value="00:00:00")

        self.create_widgets()

    def create_widgets(self):
        self.select_button = tk.Button(self, text="Sélectionner une vidéo", command=self.select_video)
        self.select_button.pack(pady=10)

        frame_extract_frame = tk.Frame(self)
        frame_extract_frame.pack(pady=5)

        tk.Label(frame_extract_frame, text="Nombre de pixels en largeur des frames:").pack(side=tk.LEFT)
        self.frame_width_entry = tk.Entry(frame_extract_frame, textvariable=self.frame_width)
        self.frame_width_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(frame_extract_frame, text="Frames par seconde (fps):").pack(side=tk.LEFT)
        self.fps_entry = tk.Entry(frame_extract_frame, textvariable=self.fps)
        self.fps_entry.pack(side=tk.LEFT, padx=5)

        self.extract_frames_button = tk.Button(self, text="Extraire les frames", command=self.extract_frames)
        self.extract_frames_button.pack(pady=5)

        frame_trim_video = tk.Frame(self)
        frame_trim_video.pack(pady=5)

        tk.Label(frame_trim_video, text="Timecode de début (hh:mm:ss):").pack(side=tk.LEFT)
        self.start_timecode_entry = tk.Entry(frame_trim_video, textvariable=self.start_timecode)
        self.start_timecode_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(frame_trim_video, text="Timecode de fin (hh:mm:ss):").pack(side=tk.LEFT)
        self.end_timecode_entry = tk.Entry(frame_trim_video, textvariable=self.end_timecode)
        self.end_timecode_entry.pack(side=tk.LEFT, padx=5)

        self.trim_video_button = tk.Button(self, text="Couper une portion de vidéo", command=self.trim_video)
        self.trim_video_button.pack(pady=5)

    def select_video(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv")])


    def extract_frames(self):
        if not self.file_path:
            messagebox.showerror("Erreur", "Veuillez sélectionner une vidéo.")
            return

        frame_width = self.frame_width.get()
        fps = self.fps.get()

        output_folder = filedialog.askdirectory()
        if not output_folder:
            return

        output_file_pattern = f"{output_folder}/frame_%04d.png"

        # Commande FFmpeg pour extraire les frames avec la dimension et le fps spécifiés
        command = f"ffmpeg -i \"{self.file_path}\" -vf \"fps={fps},scale={frame_width}:-1\" \"{output_file_pattern}\""

        try:
            subprocess.run(command, shell=True, check=True)
            messagebox.showinfo("Succès", "Frames extraites avec succès !")
        except subprocess.CalledProcessError:
            messagebox.showerror("Erreur", "Une erreur est survenue lors de l'extraction des frames.")

    def trim_video(self):
        if not self.file_path:
            messagebox.showerror("Erreur", "Veuillez sélectionner une vidéo.")
            return

        start_timecode = self.start_timecode.get()
        end_timecode = self.end_timecode.get()

        output_file = filedialog.asksaveasfilename(filetypes=[("Video files", "*.mp4")])
        if not output_file:
            return

        # Commande FFmpeg pour couper une portion de la vidéo
        command = f"ffmpeg -i \"{self.file_path}\" -ss {start_timecode} -to {end_timecode} -c:v copy \"{output_file}\""

        try:
            subprocess.run(command, shell=True, check=True, stderr=subprocess.PIPE)
            messagebox.showinfo("Succès", "Vidéo coupée avec succès !")
        except subprocess.CalledProcessError as e:
            error_output = e.stderr.decode('utf-8')
            messagebox.showerror("Erreur", f"Une erreur est survenue lors de la coupe de la vidéo.\n\n{error_output}")

if __name__ == "__main__":
    app = VideoProcessorApp()
    app.mainloop()
