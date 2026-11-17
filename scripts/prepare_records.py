"""Restore and hash-check bundled numerical records without overwriting changes."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def main():
    manifest = json.loads((ROOT / 'data/records_manifest.json').read_text(encoding='utf-8'))
    archive = ROOT / 'data/study_records.zip'
    if hashlib.sha256(archive.read_bytes()).hexdigest() != manifest['archive_sha256']:
        raise RuntimeError('The record archive failed its SHA-256 check.')
    restored = reused = 0
    with zipfile.ZipFile(archive) as handle:
        if set(handle.namelist()) != set(manifest['files']):
            raise RuntimeError('The archive member list differs from the manifest.')
        for relative, expected in manifest['files'].items():
            name = PurePosixPath(relative)
            if name.is_absolute() or '..' in name.parts or '\\' in relative or ':' in relative:
                raise RuntimeError('Unsafe archive path: ' + relative)
            target = (ROOT / relative).resolve()
            if not target.is_relative_to(ROOT):
                raise RuntimeError('Archive path leaves the repository.')
            if target.exists():
                if hashlib.sha256(target.read_bytes()).hexdigest() != expected:
                    raise RuntimeError('Existing record differs: ' + relative)
                reused += 1
                continue
            data = handle.read(relative)
            if hashlib.sha256(data).hexdigest() != expected:
                raise RuntimeError('Record hash mismatch: ' + relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open('xb') as stream:
                stream.write(data)
            restored += 1
    print(json.dumps({'passed': True, 'restored': restored, 'already_present': reused}))

if __name__ == '__main__':
    main()
