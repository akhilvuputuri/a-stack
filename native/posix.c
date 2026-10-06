#define _GNU_SOURCE
#include <node_api.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/file.h>
#include <sys/stat.h>
#include <dirent.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

static napi_value error(napi_env env) {
  char message[256]; snprintf(message,sizeof(message),"%s",strerror(errno));
  const char* code = errno==ENOENT?"ENOENT":errno==EEXIST?"EEXIST":errno==ELOOP?"ELOOP":errno==ENOTDIR?"ENOTDIR":"POSIX_ERROR";
  napi_throw_error(env,code,message); return NULL;
}
static int number(napi_env env,napi_value value) { int32_t n=0; napi_get_value_int32(env,value,&n); return n; }
static char* string(napi_env env,napi_value value) {
  size_t size=0; if(napi_get_value_string_utf8(env,value,NULL,0,&size)!=napi_ok){napi_throw_type_error(env,NULL,"Expected string");return NULL;}
  char* result=malloc(size+1); if(!result){errno=ENOMEM;error(env);return NULL;}
  napi_get_value_string_utf8(env,value,result,size+1,&size);
  if(strlen(result)!=size){free(result);napi_throw_error(env,NULL,"NUL in filesystem path");return NULL;}
  return result;
}
static napi_value integer(napi_env env,int value){napi_value out;napi_create_int32(env,value,&out);return out;}
static napi_value ok(napi_env env){napi_value out;napi_get_undefined(env,&out);return out;}
static int args(napi_env env,napi_callback_info info,napi_value* argv,size_t wanted){size_t argc=wanted;napi_get_cb_info(env,info,&argc,argv,NULL,NULL);if(argc!=wanted){napi_throw_type_error(env,NULL,"Invalid argument count");return 0;}return 1;}
static int component(napi_env env,char* name){if(!name || !*name || strchr(name,'/') || !strcmp(name,".") || !strcmp(name,"..")){napi_throw_error(env,NULL,"Invalid path component");return 0;}return 1;}
static napi_value open_dir(napi_env env,napi_callback_info info){napi_value a[1];if(!args(env,info,a,1))return NULL;char* path=string(env,a[0]);if(!path)return NULL;int fd=open(path,O_RDONLY|O_DIRECTORY|O_NOFOLLOW|O_CLOEXEC);free(path);return fd<0?error(env):integer(env,fd);}
static napi_value open_at(napi_env env,napi_callback_info info){napi_value a[4];if(!args(env,info,a,4))return NULL;char* name=string(env,a[1]);if(!component(env,name)){free(name);return NULL;}int fd=openat(number(env,a[0]),name,number(env,a[2])|O_NOFOLLOW|O_CLOEXEC,number(env,a[3]));free(name);return fd<0?error(env):integer(env,fd);}
static napi_value mkdir_at(napi_env env,napi_callback_info info){napi_value a[2];if(!args(env,info,a,2))return NULL;char* name=string(env,a[1]);if(!component(env,name)){free(name);return NULL;}int result=mkdirat(number(env,a[0]),name,0700);free(name);if(result<0 && errno!=EEXIST)return error(env);return integer(env,result==0);}
static napi_value unlink_at(napi_env env,napi_callback_info info){napi_value a[2];if(!args(env,info,a,2))return NULL;char* name=string(env,a[1]);if(!component(env,name)){free(name);return NULL;}int result=unlinkat(number(env,a[0]),name,0);free(name);if(result<0 && errno!=ENOENT)return error(env);return ok(env);}
static napi_value link_at(napi_env env,napi_callback_info info){napi_value a[3];if(!args(env,info,a,3))return NULL;char* src=string(env,a[1]);char* dst=string(env,a[2]);if(!component(env,src)||!component(env,dst)){free(src);free(dst);return NULL;}int fd=number(env,a[0]);int result=linkat(fd,src,fd,dst,0);free(src);free(dst);if(result<0){if(errno==EEXIST)return integer(env,0);return error(env);}return integer(env,1);}
static napi_value list_at(napi_env env,napi_callback_info info){napi_value a[1];if(!args(env,info,a,1))return NULL;int copy=openat(number(env,a[0]),".",O_RDONLY|O_DIRECTORY|O_CLOEXEC);if(copy<0)return error(env);DIR* directory=fdopendir(copy);if(!directory){close(copy);return error(env);}napi_value out;napi_create_array(env,&out);unsigned index=0;errno=0;struct dirent* entry;while((entry=readdir(directory))){if(!strcmp(entry->d_name,".")||!strcmp(entry->d_name,".."))continue;napi_value name;napi_create_string_utf8(env,entry->d_name,NAPI_AUTO_LENGTH,&name);napi_set_element(env,out,index++,name);}int saved=errno;closedir(directory);if(saved){errno=saved;return error(env);}return out;}
static napi_value lock_fd(napi_env env,napi_callback_info info){napi_value a[1];if(!args(env,info,a,1))return NULL;int result;do{result=flock(number(env,a[0]),LOCK_EX);}while(result<0 && errno==EINTR);return result<0?error(env):ok(env);}
static napi_value readlink_at(napi_env env,napi_callback_info info){napi_value a[2];if(!args(env,info,a,2))return NULL;char* name=string(env,a[1]);if(!component(env,name)){free(name);return NULL;}char buffer[65536];ssize_t size=readlinkat(number(env,a[0]),name,buffer,sizeof(buffer));free(name);if(size<0)return error(env);if(size==(ssize_t)sizeof(buffer)){napi_throw_error(env,NULL,"Symlink target too long");return NULL;}napi_value out;napi_create_buffer_copy(env,size,buffer,NULL,&out);return out;}
static napi_value init(napi_env env,napi_value exports){napi_property_descriptor methods[]={
 {"openDir",NULL,open_dir,NULL,NULL,NULL,napi_default_method,NULL},
 {"openAt",NULL,open_at,NULL,NULL,NULL,napi_default_method,NULL},
 {"mkdirAt",NULL,mkdir_at,NULL,NULL,NULL,napi_default_method,NULL},
 {"unlinkAt",NULL,unlink_at,NULL,NULL,NULL,napi_default_method,NULL},
 {"linkAt",NULL,link_at,NULL,NULL,NULL,napi_default_method,NULL},
 {"list",NULL,list_at,NULL,NULL,NULL,napi_default_method,NULL},
 {"lock",NULL,lock_fd,NULL,NULL,NULL,napi_default_method,NULL},
 {"readlinkAt",NULL,readlink_at,NULL,NULL,NULL,napi_default_method,NULL}};napi_define_properties(env,exports,sizeof(methods)/sizeof(methods[0]),methods);return exports;}
NAPI_MODULE(NODE_GYP_MODULE_NAME,init)
