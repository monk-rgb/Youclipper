import os
import whisper
from moviepy.editor import (
    VideoFileClip, TextClip, CompositeVideoClip,
    vfx, ColorClip
)
from moviepy.video.tools.subtitles import SubtitlesClip

class VideoClipper:
    def __init__(self):
        self.whisper_model = None

    def load_model(self, model_size="base"):
        if self.whisper_model is None:
            self.whisper_model = whisper.load_model(model_size)

    def generate_subtitles(self, video_path):
        self.load_model()
        result = self.whisper_model.transcribe(video_path)
        return result["segments"]

    def process_video(
        self,
        input_path,
        output_path,
        start_time=0,
        end_time=None,
        caption_pos="bottom",
        custom_fontsize=36,
        custom_fontcolor="white",
        custom_bg_color="black",
        effects=None,
        template_path=None,
        template_mode="overlay"
    ):
        effects = effects or []
        clip = VideoFileClip(input_path)

        if end_time and end_time <= clip.duration:
            clip = clip.subclip(start_time, end_time)
        elif start_time > 0:
            clip = clip.subclip(start_time, clip.duration)

        if "flip_horizontal" in effects:
            clip = clip.fx(vfx.mirror_x)

        if "speed_change" in effects:
            clip = clip.fx(vfx.speedx, 1.05)

        if "color_boost" in effects:
            clip = clip.fx(vfx.colorx, 1.1)

        if "zoom_in" in effects:
            w, h = clip.size
            clip = clip.crop(x1=int(w * 0.025), y1=int(h * 0.025), x2=int(w * 0.975), y2=int(h * 0.975))
            clip = clip.resize((w, h))

        pos_mapping = {
            "top": ("center", 0.1),
            "center": ("center", "center"),
            "bottom": ("center", 0.85)
        }
        subtitle_position = pos_mapping.get(caption_pos, ("center", 0.85))

        segments = self.generate_subtitles(input_path)

        subtitle_clips = []
        for seg in segments:
            s_start = seg["start"] - start_time
            s_end = seg["end"] - start_time

            if s_end <= 0 or s_start >= clip.duration:
                continue

            s_start = max(0, s_start)
            s_end = min(clip.duration, s_end)

            text_clip = TextClip(
                seg["text"].strip(),
                fontsize=custom_fontsize,
                color=custom_fontcolor,
                bg_color=custom_bg_color if custom_bg_color != "none" else None,
                font="Arial-Bold",
                method="caption",
                size=(int(clip.w * 0.8), None)
            ).set_start(s_start).set_duration(s_end - s_start).set_pos(subtitle_position)

            subtitle_clips.append(text_clip)

        clip_with_subs = CompositeVideoClip([clip] + subtitle_clips)

        if template_path and os.path.exists(template_path):
            template_clip = VideoFileClip(template_path)

            if template_mode == "background":
                template_clip = template_clip.loop(duration=clip_with_subs.duration)
                scaled_clip = clip_with_subs.resize(width=template_clip.w)
                final_clip = CompositeVideoClip([template_clip, scaled_clip.set_pos("center")])
            elif template_mode == "overlay":
                template_clip = template_clip.loop(duration=clip_with_subs.duration).resize(clip_with_subs.size)
                final_clip = CompositeVideoClip([clip_with_subs, template_clip.set_opacity(0.3)])
            else:
                final_clip = clip_with_subs
        else:
            final_clip = clip_with_subs

        final_clip.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            fps=30,
            preset="fast"
        )

        clip.close()
        final_clip.close()
        return output_path