def import_module_object(this, module):
    """指定したモジュールから公開オブジェクトをインポート

    指定したモジュールから以下をインポートする。

    1) module.__all__が指定されている場合は__all__に定義されたオブジェクト
    2) それ以外の場合は、オブジェクト名が「_」から始まらないオブジェクト

    Args:
        this (module):　インポート先のモジュール
        module (module):　インポート元のモジュール
    """

    this_dict = vars(this)
    module_dict = vars(module)

    keys = None

    if "__all__" in module_dict:
        keys = module_dict["__all__"]
    else:
        keys = [k for k in module_dict.keys() if not k.startswith("_")]

    for key in keys:
        this_dict[key] = module_dict[key]
