{
  description = "Presentation flake for demo purposes";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-23.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
  flake-utils.lib.eachDefaultSystem (system:
    let pkgs = nixpkgs.legacyPackages.${system};
    in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            graph-easy
            haskellPackages.patat
            nodejs-18_x
            python311
          ];
        };
      });
}
