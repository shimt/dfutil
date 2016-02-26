def import_module_object(this, module):
    this_dict = vars(this)
    module_dict = vars(module)

    keys = None

    if "__all__" in module_dict:
        keys = module_dict["__all__"]
    else:
        keys = [k for k in module_dict.keys() if not k.startswith("_")]

    for key in keys:
        this_dict[key] = module_dict[key]
