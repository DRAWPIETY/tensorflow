googletest移植到qnx
目的：单纯将gtest移植到qnx，默认有一些项目的依赖全部弄好了

1. 什么是交叉编译？
交叉编译：在host主机（linux）上编译出能在target（qnx）机器上执行的二进制文件。

2. 工具的准备
- 此处需要的工具有googletest发行版，项目提供的交叉编译工具链和工具链的环境配置脚本。
运行：

```
wget https://codeload.github.com/google/googletest/tar.gz/release-1.8.1
unzip googletest-release-1.8.1.tar.gz

# 当然不提出来也行，此处将googletest单独提出来了
mv googletest-release-1.8.1/googletest .
rm -rf googletest-release-1.8.1
```

- 对googletest存放位置没有特别要求，比如此处：
运行：

```
ts@ts-OptiPlex-7070:~/桌面/TEMP/googletest$ pwd
```

输出：

```
/home/ts/桌面/TEMP/googletest
```

- 登陆ftp://192.168.67.16/，账号：Octoberfest，密码: Fest123!@# 
进入tools目录下载 prebuilt_QNX700.tar.gz 和 setenv_64.sh，并将两个文件放在项目指定目录中
运行：

```
unzip prebuilt_QNX700.tar.gz
mv prebuilt_QNX700 /home/ts/桌面/TEMP/lagvm_p/qnx/

mv setenv_64.sh /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/
```

3. 交叉编译工具链的环境配置
请留意各个文件的路径
- 配置项目环境
运行：

```
ts@ts-OptiPlex-7070:~/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap$ source setenv_64.sh
```

输出：

```
QSDP_ROOT= /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/../../../prebuilt_QNX700
QSDP_FIXME_ROOT= /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/qnx_bins/prebuilt_QNX700FIXME
Local build env is:  700
Generate .gdbinit file for debugging
BSP_ROOT=/home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap
QNX_CONFIGURATION=/home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/../../../prebuilt_QNX700/.qnx
QNX_HOST=/home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/../../../prebuilt_QNX700/host/linux/x86_64
QNX_TARGET=/home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/../../../prebuilt_QNX700/target/qnx7
MAKEFLAGS=-I/home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/../../../prebuilt_QNX700/target/qnx7/usr/include -I/home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/../../../prebuilt_QNX700/target/qnx7/usr/include/mk
qnx_version=QNX_SDP700
EXCLUDE_CPULIST=arm

 Create links for prebuilt_QNX : 

lrwxrwxrwx 1 ts ts 78 8月  12 14:21 /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX -> /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/../../../prebuilt_QNX700
Generating BuildProducts.txt

 Completed Setting up Environment for 64 Bit QNX 700 Prebuilt ...
```

- 设置工具链配置
运行：

```
ts@ts-OptiPlex-7070:~/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap$ cd prebuilt_QNX

ts@ts-OptiPlex-7070:~/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX$ source qnxsdp-env.sh
```

输出：

```
QNX_HOST=/home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64
QNX_TARGET=/home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/target/qnx7
MAKEFLAGS=-I/home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/target/qnx7/usr/include
```

此处得格外注意，这里的QNX_HOST和QNX_TARGET被设置好了之后，只能在当前终端有效，若新开终端，这配置是失效的

4. 生成configure文件
利用运行source qnxsdp-env.sh的那个终端（不用这个终端就没有HOST和TARGET），去到事先下好的googletest中。
运行下面语句安装configure生成工具：
运行：

```
sudo apt-get install automake autoconf libtool

cd googletest

autoreconf  -fvi
```

输出：
```

  autoreconf  -fvi```tering directory `.'
  autoreconf: configure.ac: not using Gettext
  autoreconf: running: aclocal --force -I m4
  autoreconf: configure.ac: tracing
  autoreconf: configure.ac: creating directory build-aux
  autoreconf: running: libtoolize --copy --force
  libtoolize: putting auxiliary files in AC_CONFIG_AUX_DIR, 'build-aux'.
  libtoolize: copying file 'build-aux/ltmain.sh'
  libtoolize: putting macros in AC_CONFIG_MACRO_DIRS, 'm4'.
  libtoolize: copying file 'm4/libtool.m4'
  libtoolize: copying file 'm4/ltoptions.m4'
  libtoolize: copying file 'm4/ltsugar.m4'
  libtoolize: copying file 'm4/ltversion.m4'
  libtoolize: copying file 'm4/lt~obsolete.m4'
  autoreconf: running: /usr/bin/autoconf --force
  autoreconf: running: /usr/bin/autoheader --force
  autoreconf: running: automake --add-missing --copy --force-missing
  configure.ac:27: installing 'build-aux/compile'
  configure.ac:30: installing 'build-aux/config.guess'
  configure.ac:30: installing 'build-aux/config.sub'
  configure.ac:24: installing 'build-aux/install-sh'
  configure.ac:24: installing 'build-aux/missing'
  Makefile.am: installing 'build-aux/depcomp'
  parallel-tests: installing 'build-aux/test-driver'
  autoreconf: Leaving directory `.'
```


5. 配置编译环境并编译
运行：

```
ts@ts-OptiPlex-7070:~/桌面/TEMP/googletest$ ./configure --prefix=/home/ts/桌面/TEMP/googletest/build --host=arm --build=i686-pc-linux CC=/home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-gcc CXX=/home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-g++ CXXFLAGS=-std=gnu++14 --disable-shared
```

输出：

```
checking for a BSD-compatible install... /usr/bin/install -c
checking whether build environment is sane... yes
checking for arm-strip... no
checking for strip... strip
configure: WARNING: using cross tools not prefixed with host triplet
checking for a thread-safe mkdir -p... /bin/mkdir -p
checking for gawk... no
checking for mawk... mawk
checking whether make sets $(MAKE)... yes
checking whether make supports nested variables... yes
checking for arm-gcc... /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-gcc
checking whether the C compiler works... yes
checking for C compiler default output file name... a.out
checking for suffix of executables... 
checking whether we are cross compiling... yes
checking for suffix of object files... o
checking whether we are using the GNU C compiler... yes
checking whether /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-gcc accepts -g... yes
checking for /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-gcc option to accept ISO C89... none needed
checking whether /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-gcc understands -c and -o together... yes
checking for style of include used by make... GNU
checking dependency style of /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-gcc... gcc3
checking whether we are using the GNU C++ compiler... yes
checking whether /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-g++ accepts -g... yes
checking dependency style of /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-g++... gcc3
checking build system type... i686-pc-linux-gnu
checking host system type... arm-unknown-none
checking how to print strings... printf
checking for a sed that does not truncate output... /bin/sed
checking for grep that handles long lines and -e... /bin/grep
checking for egrep... /bin/grep -E
checking for fgrep... /bin/grep -F
checking for ld used by /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-gcc... /home/ts/桌面/TEMP/lagvm_p/qnx/prebuilt_QNX700/host/linux/x86_64/usr/bin/arm-unknown-nto-qnx7.0.0eabi-ld
checking if the linker (/home/ts/桌面/TEMP/lagvm_p/qnx/prebuilt_QNX700/host/linux/x86_64/usr/bin/arm-unknown-nto-qnx7.0.0eabi-ld) is GNU ld... yes
checking for BSD- or MS-compatible name lister (nm)... no
checking for arm-dumpbin... no
checking for arm-link... no
checking for dumpbin... no
checking for link... link -dump
checking the name lister (nm) interface... BSD nm
checking whether ln -s works... yes
checking the maximum length of command line arguments... 1572864
checking how to convert i686-pc-linux-gnu file names to arm-unknown-none format... func_convert_file_noop
checking how to convert i686-pc-linux-gnu file names to toolchain format... func_convert_file_noop
checking for /home/ts/桌面/TEMP/lagvm_p/qnx/prebuilt_QNX700/host/linux/x86_64/usr/bin/arm-unknown-nto-qnx7.0.0eabi-ld option to reload object files... -r
checking for arm-objdump... no
checking for objdump... objdump
checking how to recognize dependent libraries... unknown
checking for arm-dlltool... no
checking for dlltool... no
checking how to associate runtime and link libraries... printf %s\n
checking for arm-ar... no
checking for ar... ar
checking for archiver @FILE support... @
checking for arm-strip... strip
checking for arm-ranlib... no
checking for ranlib... ranlib
checking command to parse nm output from /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-gcc object... ok
checking for sysroot... no
checking for a working dd... /bin/dd
checking how to truncate binary pipes... /bin/dd bs=4096 count=1
checking for arm-mt... no
checking for mt... mt
checking if mt is a manifest tool... no
checking how to run the C preprocessor... /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-gcc -E
checking for ANSI C header files... yes
checking for sys/types.h... yes
checking for sys/stat.h... yes
checking for stdlib.h... yes
checking for string.h... yes
checking for memory.h... yes
checking for strings.h... yes
checking for inttypes.h... yes
checking for stdint.h... yes
checking for unistd.h... yes
checking for dlfcn.h... yes
checking for objdir... .libs
checking if /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-gcc supports -fno-rtti -fno-exceptions... no
checking for /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-gcc option to produce PIC... -fPIC -DPIC
checking if /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-gcc PIC flag -fPIC -DPIC works... yes
checking if /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-gcc static flag -static works... yes
checking if /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-gcc supports -c -o file.o... yes
checking if /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-gcc supports -c -o file.o... (cached) yes
checking whether the /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-gcc linker (/home/ts/桌面/TEMP/lagvm_p/qnx/prebuilt_QNX700/host/linux/x86_64/usr/bin/arm-unknown-nto-qnx7.0.0eabi-ld) supports shared libraries... yes
checking dynamic linker characteristics... no
checking how to hardcode library paths into programs... immediate
checking whether stripping libraries is possible... yes
checking if libtool supports shared libraries... no
checking whether to build shared libraries... no
checking whether to build static libraries... yes
checking how to run the C++ preprocessor... /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-g++ -E
checking for ld used by /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-g++... /home/ts/桌面/TEMP/lagvm_p/qnx/prebuilt_QNX700/host/linux/x86_64/usr/bin/arm-unknown-nto-qnx7.0.0eabi-ld
checking if the linker (/home/ts/桌面/TEMP/lagvm_p/qnx/prebuilt_QNX700/host/linux/x86_64/usr/bin/arm-unknown-nto-qnx7.0.0eabi-ld) is GNU ld... yes
checking whether the /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-g++ linker (/home/ts/桌面/TEMP/lagvm_p/qnx/prebuilt_QNX700/host/linux/x86_64/usr/bin/arm-unknown-nto-qnx7.0.0eabi-ld) supports shared libraries... no
checking for /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-g++ option to produce PIC... -fPIC -DPIC
checking if /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-g++ PIC flag -fPIC -DPIC works... yes
checking if /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-g++ static flag -static works... yes
checking if /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-g++ supports -c -o file.o... yes
checking if /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-g++ supports -c -o file.o... (cached) yes
checking whether the /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-g++ linker (/home/ts/桌面/TEMP/lagvm_p/qnx/prebuilt_QNX700/host/linux/x86_64/usr/bin/arm-unknown-nto-qnx7.0.0eabi-ld) supports shared libraries... no
checking dynamic linker characteristics... no
checking how to hardcode library paths into programs... immediate
checking for python... /home/ts/桌面/TEMP/lagvm_p/qnx/prebuilt_QNX700/host/linux/x86_64/usr/bin/python
checking for the pthreads library -lpthreads... no
checking whether pthreads work without any flags... yes
checking for joinable pthread attribute... PTHREAD_CREATE_JOINABLE
checking if more special flags are required for pthreads... no
checking whether to check for GCC pthread/shared inconsistencies... yes
checking whether -pthread is sufficient with -shared... yes
checking that generated files are newer than configure... done
configure: creating ./config.status
config.status: creating Makefile
config.status: creating scripts/gtest-config
config.status: creating build-aux/config.h
config.status: executing depfiles commands
config.status: executing libtool commands
```

运行：

```
ts@ts-OptiPlex-7070:~/桌面/TEMP/googletest$ make
```

输出

```
depbase=`echo src/gtest-all.lo | sed 's|[^/]*$|.deps/&|;s|\.lo$||'`;\
/bin/bash ./libtool  --tag=CXX   --mode=compile /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-g++ -DHAVE_CONFIG_H -I. -I./build-aux  -I. -I./include  -DGTEST_HAS_PTHREAD=1 -std=gnu++14 -MT src/gtest-all.lo -MD -MP -MF $depbase.Tpo -c -o src/gtest-all.lo src/gtest-all.cc &&\
mv -f $depbase.Tpo $depbase.Plo
libtool: compile:  /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-g++ -DHAVE_CONFIG_H -I. -I./build-aux -I. -I./include -DGTEST_HAS_PTHREAD=1 -std=gnu++14 -MT src/gtest-all.lo -MD -MP -MF src/.deps/gtest-all.Tpo -c src/gtest-all.cc -o src/gtest-all.o
/bin/bash ./libtool  --tag=CXX   --mode=link /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-g++ -DGTEST_HAS_PTHREAD=1 -std=gnu++14   -o lib/libgtest.la -rpath /home/ts/桌面/TEMP/googletest/build/lib src/gtest-all.lo  
libtool: link: ar cru lib/.libs/libgtest.a  src/gtest-all.o
ar: `u' modifier ignored since `D' is the default (see `U')
libtool: link: ranlib lib/.libs/libgtest.a
libtool: link: ( cd "lib/.libs" && rm -f "libgtest.la" && ln -s "../libgtest.la" "libgtest.la" )
depbase=`echo src/gtest_main.lo | sed 's|[^/]*$|.deps/&|;s|\.lo$||'`;\
/bin/bash ./libtool  --tag=CXX   --mode=compile /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-g++ -DHAVE_CONFIG_H -I. -I./build-aux  -I. -I./include  -DGTEST_HAS_PTHREAD=1 -std=gnu++14 -MT src/gtest_main.lo -MD -MP -MF $depbase.Tpo -c -o src/gtest_main.lo src/gtest_main.cc &&\
mv -f $depbase.Tpo $depbase.Plo
libtool: compile:  /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-g++ -DHAVE_CONFIG_H -I. -I./build-aux -I. -I./include -DGTEST_HAS_PTHREAD=1 -std=gnu++14 -MT src/gtest_main.lo -MD -MP -MF src/.deps/gtest_main.Tpo -c src/gtest_main.cc -o src/gtest_main.o
/bin/bash ./libtool  --tag=CXX   --mode=link /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-g++ -DGTEST_HAS_PTHREAD=1 -std=gnu++14   -o lib/libgtest_main.la -rpath /home/ts/桌面/TEMP/googletest/build/lib src/gtest_main.lo lib/libgtest.la 
libtool: link: ar cru lib/.libs/libgtest_main.a  src/gtest_main.o
ar: `u' modifier ignored since `D' is the default (see `U')
libtool: link: ranlib lib/.libs/libgtest_main.a
libtool: link: ( cd "lib/.libs" && rm -f "libgtest_main.la" && ln -s "../libgtest_main.la" "libgtest_main.la" )
```

至此编译结束

6. 编译好静态库的利用

```
ts@ts-OptiPlex-7070:~/桌面/TEMP/googletest$ ls lib/.libs
libgtest.a  libgtest.la  libgtest.lai  libgtest_main.a  libgtest_main.la  libgtest_main.lai

ts@ts-OptiPlex-7070:~/桌面/TEMP/googletest$ ls include/gtest
gtest-death-test.h  gtest.h  gtest-message.h  gtest-param-test.h  gtest-param-test.h.pump  gtest_pred_impl.h  gtest-printers.h  gtest_prod.h  gtest-spi.h  gtest-test-part.h  gtest-typed-test.h  internal
```

.a 为静态库，可以是一个或多个.o合在一起,用于静态连接

项目主要利用lib/.libs/libgtest.a和lib/.libs/libgtest_main.a这两个静态库文件与include/gtest头文件目录，将这两个.a文件和gtest目录拷贝到需要的项目中

7. 例子
以下方式常用：

```
g++ main.c -lstatic -L/home/gec/lib -I/home/gec/include -o target
```

- /home/gec/lib—>存放 libstatic.a 文件
- /home/gec/include—>存放 add.h sub.h
- -l(小写的L) ，后面跟库的名称，static就是libstatic.a 的名称
- -L —>指定库文件的路径，加路径时可空格，也可不空格
- -I —>指定头文件的路径，加路径时可空格，也可不空格  
示例：

```
ntoarmv7-g++ test.cc -lgtest -o test.out -L /home/ts/11/staticlib -I /home/ts/11
```

将gtest 和两个.a文件拷贝出来，再写一个test.cc试一下
运行：

```
ts@ts-OptiPlex-7070:~/11$ ls
```

输出：

```
gtest  staticlib  test.cc
test.cc
#include <gtest/gtest.h>

int add(int a, int b)
{
        return a+b;
}

TEST(testcase, test0)
{
        EXPECT_EQ(add(2, 3), 5);
}

int main(int argc, char **argv)
{
        testing::InitGoogleTest(&argc, argv);
        return RUN_ALL_TESTS();
}
```

编译(source一下QNX_HOST、QNX_TARGETd的终端来编译）：

```
ts@ts-OptiPlex-7070:~/11$ /home/ts/桌面/TEMP/lagvm_p/qnx/qcom_qnx/apps/qnx_ap/prebuilt_QNX/host/linux/x86_64/usr/bin/ntoarmv7-g++ test.cc -lgtest -o test.out -L /home/ts/11/staticlib -I /home/ts/11
```

运行

```
ts@ts-OptiPlex-7070:~/11$ ls
```

输出

```
gtest  staticlib  test.cc  test.out
```
