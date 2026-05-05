def compare_files(current, baseline):
    changes = []

    # Check deleted & modified
    for file in baseline:
        if file not in current:
            changes.append(("Deleted", file))
        elif baseline[file] != current[file]:
            changes.append(("Modified", file))

    # Check new files
    for file in current:
        if file not in baseline:
            changes.append(("New", file))

    return changes