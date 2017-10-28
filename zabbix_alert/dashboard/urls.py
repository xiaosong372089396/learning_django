from django.conf.urls import url,include
from views import getCpuState,getMemoryState
urlpatterns = [
    url(r'get_cpu_state/$',getCpuState,name="get_cpu_state" ),
    url(r'get_memory_state/$',getMemoryState,name="get_memory_state" ),
]