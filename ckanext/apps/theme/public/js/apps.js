function confirmDelete() {
    var _continue=confirm("Are you sure you want to delete this submission?")
    if (_continue)
        return true;
    return false;
}