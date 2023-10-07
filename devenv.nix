{pkgs, ...}: {
  # packages = [
  #
  # ];
  dotenv.enable = true;

  # https://devenv.sh/languages/
  languages = {
    nix.enable = true;
    python = {
      enable = true;
      version = "3.12";
      poetry = {
        enable = true;
        activate.enable = true;
      };
    };
  };

  # https://devenv.sh/pre-commit-hooks/
  pre-commit.hooks = {
    shellcheck.enable = true;
    alejandra.enable = true;
    statix.enable = true;
    black.enable = true;
    ruff.enable = true;
  };
}
