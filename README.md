# et-prebuild (pilot)
Prebuilds 80 random Endless-Terminals task environments and pushes them as tags
of a single GHCR package `ghcr.io/simonucl/et-envs:<taskid>`, so aks-modal can
pull them by ref (no per-trial Dockerfile replay). Source: obiwan96/endless-terminals.
