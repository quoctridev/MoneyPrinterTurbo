import os
import shutil
import socket

import toml
from loguru import logger

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
config_file = f"{root_dir}/config.toml"



def load_config():
    # Nếu config.toml chưa tồn tại → tạo từ bản mẫu
    if not os.path.isfile(config_file):
        example_file = f"{root_dir}/config.example.toml"
        if os.path.isfile(example_file):
            try:
                shutil.copyfile(example_file, config_file)
                logger.info(" Đã tạo config.toml từ config.example.toml")
            except Exception as e:
                logger.error(f" Lỗi khi copy config: {e}")
                raise
        else:
            logger.error(" Không tìm thấy config.example.toml để tạo config.toml")
            raise FileNotFoundError("Thiếu cả config.toml và config.example.toml")

    logger.info(f" Load config từ file: {config_file}")

    # Load file TOML
    try:
        _config_ = toml.load(config_file)
    except Exception as e:
        logger.warning(f" Lỗi load config (utf-8): {str(e)}, thử lại bằng utf-8-sig")
        with open(config_file, mode="r", encoding="utf-8-sig") as fp:
            _cfg_content = fp.read()
            _config_ = toml.loads(_cfg_content)
    return _config_

    # Load file TOML
    try:
        _config_ = toml.load(config_file)
    except Exception as e:
        logger.warning(f"Lỗi khi load config (utf-8): {str(e)}, thử lại bằng utf-8-sig...")
        with open(config_file, mode="r", encoding="utf-8-sig") as fp:
            _cfg_content = fp.read()
            _config_ = toml.loads(_cfg_content)
    return _config_


def save_config():
    with open(config_file, "w", encoding="utf-8") as f:
        _cfg["app"] = app
        _cfg["azure"] = azure
        _cfg["siliconflow"] = siliconflow
        _cfg["gemini"] = gemini
        _cfg["ui"] = ui
        f.write(toml.dumps(_cfg))


_cfg = load_config()
app = _cfg.get("app", {})
whisper = _cfg.get("whisper", {})
proxy = _cfg.get("proxy", {})
gemini = _cfg.get("gemini", {})
azure = _cfg.get("azure", {})
siliconflow = _cfg.get("siliconflow", {})
ui = _cfg.get(
    "ui",
    {
        "hide_log": False,
    },
)

hostname = socket.gethostname()

log_level = _cfg.get("log_level", "DEBUG")
listen_host = _cfg.get("listen_host", "0.0.0.0")
listen_port = _cfg.get("listen_port", 8080)
project_name = _cfg.get("project_name", "MoneyPrinterTurbo")
project_description = _cfg.get(
    "project_description",
    "<a href='https://github.com/harry0703/MoneyPrinterTurbo'>https://github.com/harry0703/MoneyPrinterTurbo</a>",
)
project_version = _cfg.get("project_version", "1.2.6")
reload_debug = False

imagemagick_path = app.get("imagemagick_path", "")
if imagemagick_path and os.path.isfile(imagemagick_path):
    os.environ["IMAGEMAGICK_BINARY"] = imagemagick_path

ffmpeg_path = app.get("ffmpeg_path", "")
if ffmpeg_path and os.path.isfile(ffmpeg_path):
    os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path

logger.info(f"{project_name} v{project_version}")
