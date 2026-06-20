{
  description = "Development shell for system-design implementation drills";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { nixpkgs, ... }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "aarch64-darwin"
        "x86_64-darwin"
      ];
      forAllSystems = nixpkgs.lib.genAttrs systems;
    in {
      devShells = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
        in {
          default = pkgs.mkShell {
            packages = [
              pkgs.python3
            ];

            shellHook = ''
              echo "system-design dev shell"
              echo "Try: python3 implementations/rate-limiter-lab/test_rate_limiter.py"
              echo "Try: python3 implementations/consistent-hashing-lab/test_consistent_hash.py"
            '';
          };
        });
    };
}
