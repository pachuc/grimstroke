import argparse

from flow_field import FlowField


def main(args):
  if args.fullscreen:
    p = FlowField(config_path=args.config)
  else:
    p = FlowField(fullscreen=False, width=args.width, height=args.height, config_path=args.config)
  p.run()

def validate_args(parser):
  args = parser.parse_args()

  if args.fullscreen:
    if args.width is not None or args.height is not None:
      parser.error("Cannot use width and height arguments in fullscreen mode.")
  else:
    if args.width is None or args.height is None:
      parser.error("Must specify width and height when not running in fullscreen mode.")

  return args

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fullscreen", help="Run in full screen mode", action="store_true")
    parser.add_argument("--width", help="Specify window width", type=int)
    parser.add_argument("--height", help="Specify window height", type=int)
    parser.add_argument("--config", help="Path to config file that should be used", action="store", default=None)
    args = validate_args(parser)
    main(args)
