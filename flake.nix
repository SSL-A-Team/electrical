{
  description = "The firmware repository for the SSL A-Team.";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, rust-overlay, flake-utils }:
    flake-utils.lib.eachSystem [
        "aarch64-linux"
        "aarch64-darwin"
        # "i686-linux" # gcc10 doesn't seem to have support in the Nix repos
        "x86_64-darwin"
        "x86_64-linux" ]
    (system: 
      let 

        pkgs = import nixpkgs {
          inherit system; 
        };

        python = "python39";

        packageName = "ateam-electrical";

      in {
        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            # Kicad
            kicad

            # ngSpice
            ngspice

            # Python
            (pkgs.${python}.withPackages
              (ps: with ps; [ numpy matplotlib ]))
          ];
        };
      }
    );
}
