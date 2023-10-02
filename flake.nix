{
  description = "The firmware repository for the SSL A-Team.";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachSystem [
        "aarch64-linux"
        "aarch64-darwin"
        "x86_64-darwin"
        "x86_64-linux" ]
    (system: 
      let 

        pkgs = import nixpkgs {
          inherit system; 
        };

        python = "python310";

        packageName = "ateam-electrical";

      in {
        devShells.default = pkgs.mkShell {

          shellHook = ''
            source $(realpath ./.)/nix-shell-setup.bash
          '';

          buildInputs = with pkgs; [
            # Python
            (pkgs.${python}.withPackages
              (ps: with ps; [ numpy matplotlib scipy ]))
            poetry
          ];
        };

        devShells.cad = pkgs.mkShell {

          shellHook = ''
            source $(realpath ./.)/nix-shell-setup.bash
          '';

          buildInputs = with pkgs; [
            # KiCad
            kicad

            # Python
            (pkgs.${python}.withPackages
              (ps: with ps; [ numpy matplotlib scipy ]))
            poetry
          ];
        };
      }
    );
}
