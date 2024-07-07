from flask import Response
from flask.views import MethodView


class ViewSet():

    def __init__(self, url_prefix, list_func = None, post_func = None, 
                 retrieve_func = None, put_func = None, patch_func = None,
                 delete_func = None) -> None:
        
        self.url_prefix = url_prefix
        self.list_func = list_func
        self.post_func = post_func
        self.retrieve_func = retrieve_func
        self.put_func = put_func
        self.patch_func = patch_func
        self.delete_func = delete_func

    def __repr__(self) -> str:
        return f'ViewSet with url - {self.url_prefix}'
    
    def check_exist_method(self, func: str, pk: int = None):
        function = getattr(self, func)
        if function:
            if pk:
                return function(pk)
            else:
                return function()
        else:
            return Response("Method not allowed", 405)
    
    
    class GroupAPI(MethodView):
        
        def __init__(self, viewset) -> None:
            self.viewset: ViewSet = viewset
        
        def get(self):
            return self.viewset.check_exist_method("list_func")

        def post(self):
            return self.viewset.check_exist_method("post_func")

    
    class ItemAPI(MethodView):
        
        def __init__(self, viewset) -> None:
            self.viewset: ViewSet = viewset
        
        def get(self, pk):
            return self.viewset.check_exist_method("retrieve_func", pk)

        def put(self, pk):
            return self.viewset.check_exist_method("put_func", pk)

        def patch(self, pk):
            return self.viewset.check_exist_method("patch_func", pk)

        def delete(self, pk):
            return self.viewset.check_exist_method("delete_func", pk)
