{
  description = "Useful dev tools for platform development";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-23.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        pythonPackages = (ps: [
          ps.debugpy
          ps.hypothesis
          ps.pydantic
          ps.pytest
          ps.pytest-golden
          ps.setuptools
        ]);
        python = pkgs.python310.withPackages pythonPackages;
      in
      {
        devShells.default = pkgs.mkShell {
          name = "platform-dev-shell";
          buildInputs = [
            pkgs.mutmut
            python
            pkgs.black
          ];
        };
      });
}
