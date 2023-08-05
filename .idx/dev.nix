{pkgs}: {

  # Which nixpkgs channel to use.
  channel = "stable-23.05"; # or "unstable"

  # Use https://search.nixos.org/packages to  find packages
  packages = [
    
  ];

  # search for the extension on https://open-vsx.org/ and use "publisher.id"
  idx.extensions = [
    "vscodevim.vim"
    "ms-python.python"
  ];
}