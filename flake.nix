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
            # Kicad. This has an insane build time, so maybe make folks download precached bins.
            # kicad

            # ngSpice
            # ngspice

            # Python
            python
            poetry
          ];
        };
      }
    );
}
