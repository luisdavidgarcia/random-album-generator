#!/usr/bin/env python3
from __future__ import annotations

import random
import tarfile
import logging
import shutil
from pathlib import Path
from dataclasses import dataclass
import argparse


@dataclass(frozen=True)
class Config:
    source: Path
    destination: Path
    max_size: int
    extensions: set[str]
    verbose: bool


def setup_logging(verbose: bool) -> None:
    logging_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
            level=logging_level,
            format='%(asctime)s - %(levelname)s - %(message)s'
    )


def get_all_albums(directory: Path) -> list[Path]:
    return [d for d in directory.iterdir() if d.is_dir()]


def get_files_from_album(album: Path, extensions: set[str]) -> list[Path]:
    return [
        f for f in album.rglob("*")
        if f.is_file()
        and f.suffix.lower() in extensions
        and not f.name.startswith(".")
    ]


def select_random_files(albums: list[Path], cfg: Config) -> list[Path]:
    random.shuffle(albums)

    total_size = 0
    selected_files: list[Path] = []
    visited_files: set[Path] = set()

    for album in albums:
        files = [f for f in get_files_from_album(album, cfg.extensions)
                 if f not in visited_files]

        if not files:
            continue

        random.shuffle(files)

        num_files_to_select = random.randint(1, 6)

        for f in files[:num_files_to_select]:
            size = f.stat().st_size

            if total_size + size > cfg.max_size:
                return selected_files

            selected_files.append(f)
            visited_files.add(f)
            total_size += size

    return selected_files


def create_random_album(cfg: Config) -> None:
    setup_logging(cfg.verbose)

    albums = get_all_albums(cfg.source)
    if not albums:
        logging.error("No albums found.")
        return

    selected_files = select_random_files(albums, cfg)
    if not selected_files:
        logging.warning((
            "No files selected. Try increasing max_size or",
            "checking extensions."))
        return

    total_size = sum(f.stat().st_size for f in selected_files)
    logging.info(f"Selected {len(selected_files)} files,")
    logging.info(
            f"Total album size: {total_size / (1024 * 1024 * 1024):.2f} GB"
    )

    archive = archive_album(selected_files, cfg.destination)
    logging.info(f"Created archive: {archive}")


def archive_album(files: list[Path], destination: Path) -> Path:
    destination.mkdir(parents=True, exist_ok=True)

    videos_directory = destination / "videos"
    videos_directory.mkdir(parents=True, exist_ok=True)

    photos_directory = destination / "photos"
    photos_directory.mkdir(parents=True, exist_ok=True)

    for f in files:
        if f.suffix.lower() in [".jpg", ".jpeg"]:
            shutil.copy(f, photos_directory / f.name)
        elif f.suffix.lower() == ".mp4":
            shutil.copy(f, videos_directory / f.name)

    archive = destination.parent / "archive.tar.gz"

    with tarfile.open(archive, "w:gz") as tar:
        for f in files:
            tar.add(f, arcname=f.name)

    return archive


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a random album with size limits.")
    parser.add_argument("source")
    parser.add_argument("destination")
    parser.add_argument("--max_size", type=int, default=1024**3)
    parser.add_argument("--extensions", nargs="*",
                        default=[".jpg", ".jpeg", ".png", ".mp4"])
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()

    cfg = Config(
            source=Path(args.source),
            destination=Path(args.destination),
            max_size=args.max_size,
            extensions=set(args.extensions),
            verbose=args.verbose,
    )

    if not cfg.destination.exists():
        cfg.destination.mkdir(parent=True)

    if not cfg.destination.is_dir():
        raise SystemExit("Destination must be a directory")

    create_random_album(cfg)


if __name__ == "__main__":
    main()
