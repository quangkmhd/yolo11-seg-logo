import argparse
import sys
from src.logo_seg.utils.logger import setup_logger
from src.logo_seg.config import Config

def main():
    parser = argparse.ArgumentParser(description="YOLO11 Logo Segmentation Production CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Data Command
    data_parser = subparsers.add_parser("data", help="Data processing commands")
    data_subparsers = data_parser.add_subparsers(dest="subcommand", help="Data subcommands")
    
    # Data Process
    process_parser = data_subparsers.add_parser("process", help="Move files from source folders")
    process_parser.add_argument("--sources", nargs="+", help="Source folder paths")
    
    # Data Convert
    convert_parser = data_subparsers.add_parser("convert", help="Convert labelme JSON to YOLO segmentation")
    convert_parser.add_argument("--train-split", type=float, default=0.8, help="Train split ratio")

    # Train Command
    train_parser = subparsers.add_parser("train", help="Train the model")

    # Predict Command
    predict_parser = subparsers.add_parser("predict", help="Run inference")
    predict_parser.add_argument("--source", required=True, help="Path to image or video")
    predict_parser.add_argument("--model", help="Path to model checkpoint")

    # Serve Command
    serve_parser = subparsers.add_parser("serve", help="Launch Gradio web app")
    serve_parser.add_argument("--port", type=int, default=7860, help="Gradio port")

    args = parser.parse_args()
    logger = setup_logger("cli")

    if args.command == "data":
        if args.subcommand == "process":
            from src.logo_seg.data.preprocessor import move_files_safe
            sources = args.sources or ["/home/quangnhvn34/fsoft/detect/data_logo_zip/dhl_23_12"]
            move_files_safe(sources, str(Config.SOURCE_DATA_DIR))
        elif args.subcommand == "convert":
            from src.logo_seg.data.converter import LabelmeToYoloConverter
            converter = LabelmeToYoloConverter(str(Config.SOURCE_DATA_DIR), str(Config.OUTPUT_DATA_DIR))
            converter.run(train_split=args.train_split)
            
    elif args.command == "train":
        from src.logo_seg.models.trainer import train_model
        train_model()
        
    elif args.command == "predict":
        from src.logo_seg.models.predictor import Predictor
        predictor = Predictor(args.model)
        results = predictor.predict(args.source)
        for result in results:
            # Add custom result handling here
            pass
            
    elif args.command == "serve":
        from src.logo_seg.app.interface import create_app
        logger.info(f"Starting Gradio server on port {args.port}...")
        app = create_app()
        app.launch(server_port=args.port)
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
