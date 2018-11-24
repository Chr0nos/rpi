function form_change(form) {
    console.log("changed !");
    ajax = new AjaxForm(form, false);
    ajax.send();
    return false;
}
