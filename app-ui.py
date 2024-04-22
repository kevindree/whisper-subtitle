import traceback
import gradio as gr
import whisper
from whisper.utils import get_writer
from utilities import get_output_file_path, get_youtube_audio_file_path

# file_path: file directory + file name
# file_dir: file directory only
# file_name: file name without directory information
# file_basename: file name without extension


model = whisper.load_model("medium")


def audio_transcribe(chosen_file_type, audio_file, video_file, youtube_url):
    if chosen_file_type == "Audio" and len(audio_file) > 0:
        input_file_path = audio_file
    elif chosen_file_type == "Video" and len(video_file) > 0:
        input_file_path = video_file
    else:
        input_file_path = get_youtube_audio_file_path(youtube_url)

    output_file_dir, output_file_name = get_output_file_path(input_file_path, ".srt")
    output_file_path = output_file_dir + output_file_name
    print(f"out file path: {output_file_path}")

    # 进行语音识别
    result = model.transcribe(input_file_path)

    # 设定写文件工具 及 参数
    writer = get_writer("srt", output_file_dir)

    try:
        # 使用写文件参数写文件
        writer(result, output_file_name, {})
        print("Transcribe successes.")
    except Exception as e:
        traceback.print_exc()
        print(f"Failed while writing file {output_file_name} due to {type(e).__name__}: {str(e)}")

    with open(output_file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    print(f"File path: {output_file_path}")

    # 返回输出值
    return {
        output_file_content: gr.TextArea(value=file_content),
        output_file_download: gr.File(label=f"下载 {output_file_name}", value=output_file_path, visible=True)
    }


# 根据选择的文件类型，变更页面显示的输入内容
def on_change_file_type(value):
    if value == "Audio":
        return {
            input_audio_file: gr.Audio(visible=True),
            input_video_file: gr.Video(visible=False),
            youtube_row: gr.Column(visible=False)
        }
    elif value == "Video":
        return {
            input_audio_file: gr.Audio(visible=False),
            input_video_file: gr.Video(visible=True),
            youtube_row: gr.Column(visible=False)
        }
    elif value == "Youtube url":
        return {
            input_audio_file: gr.Audio(visible=False),
            input_video_file: gr.Video(visible=False),
            youtube_row: gr.Column(visible=True)
        }


def download_youtube_audio(youtube_url):
    input_file_path = get_youtube_audio_file_path(youtube_url)
    if input_file_path == "Error":
        return [
            gr.Audio(visible=False),
            gr.Text(value="Error:Invalid Youtube url!", visible=True)
        ]
    else:
        return [
            gr.Audio(value=input_file_path, visible=True),
            gr.Text(visible=False)
        ]


# 界面主体内容
with gr.Blocks(theme=gr.themes.Default(primary_hue="red", secondary_hue="pink")) as interface:
    with gr.Row(equal_height=True):
        with gr.Column(min_width=600):
            file_type = gr.Dropdown(
                choices=["Audio", "Video", "Youtube url"],
                value="Audio",
                label="文件类型",
                info="选择你要生成字幕的文件类型.",
                filterable=False
            )
            input_audio_file = gr.Audio(
                label="上载语音文件",
                sources=["upload"],
                type="filepath",
                visible=True
            )
            input_video_file = gr.Video(
                label="上载视频文件",
                sources=["upload"],
                visible=False
            )
            with gr.Row(equal_height=True, visible=False) as youtube_row:
                with gr.Column(scale=3):
                    input_youtube_url = gr.Textbox(
                        label="Youtube视频地址"
                    )
                download_youtube_btn = gr.Button("获取Youtube音频", scale=1)
            input_youtube_audio_file = gr.Audio(visible=False)
            error_message = gr.Text(visible=False)
            submit_btn = gr.Button("开始生成字幕")

        with gr.Column(min_width=600):
            output_file_content = gr.TextArea(
                label="输出字幕文本内容",
                autoscroll=False,
                show_label=True
            )
            output_file_download = gr.DownloadButton(visible=False)

        download_youtube_btn.click(download_youtube_audio, input_youtube_url, [input_youtube_audio_file, error_message])

        file_type.change(fn=on_change_file_type,
                         inputs=file_type,
                         outputs=[input_audio_file, input_video_file, youtube_row]
                         )
        submit_btn.click(fn=audio_transcribe,
                         inputs=[file_type, input_audio_file, input_video_file, input_youtube_url],
                         outputs=[output_file_content, output_file_download]
                         )

if __name__ == "__main__":
    interface.launch()
