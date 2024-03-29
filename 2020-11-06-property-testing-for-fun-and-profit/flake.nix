{
  description = "Useful dev tools for platform development";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-22.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        nodeJS = pkgs.nodejs-19_x;
        yarn = pkgs.nodePackages.yarn;
        python3Packages = (ps: [
          ps.hypothesis
          ps.pytest
        ]);
        python = pkgs.python311.withPackages python3Packages;
      in
      {
        devShells.default = pkgs.mkShell {
          name = "platform-dev-shell";
          buildInputs = [ nodeJS python yarn ];
        };
      });
}
