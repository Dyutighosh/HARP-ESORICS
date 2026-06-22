



from typing import Union, List, Dict, Tuple
from pathlib import Path
import sys
import os
import re
import glob
import shutil
import sysconfig
import platform
import subprocess
import toml
from packaging.version import Version


from setuptools import setup, Extension, find_packages


platform_system = platform.system()


config = toml.load("pyproject.toml")
project_config = config['project']
project_name = project_config['name']




VERSION = project_config['version']
def re_sub_file(regex: str, replace: str, filename: str):

    with open(filename) as sub_file:
        file_string = sub_file.read()
    with open(filename, 'w') as sub_file:
        sub_file.write(re.sub(regex, '{}'.format(replace), file_string))


V_README_REGEX = r'(?<=\*\*Version\*\* \| )[0-9]+\.[0-9]+\.[0-9a-z]+'
V_INIT_REGEX = r'(?<=__version__ = \")[0-9]+\.[0-9]+\.[0-9a-z]+(?=\")'
re_sub_file(regex=V_README_REGEX, replace=VERSION, filename='README.md')
re_sub_file(regex=V_INIT_REGEX, replace=VERSION, filename='Pyfhel/__init__.py')




CYTHONIZE = False
try:
    from Cython.Build import cythonize
    CYTHONIZE = True
except ImportError:
    pass


COVERAGE = False
if '.cov' in os.listdir():
    print("  [COVERAGE=True] `.cov` file detected. Building with coverage support.")
    COVERAGE = True






def _pl(args: List[Union[str,dict]]) -> List[str]:

    args_pl = []
    for arg in args:
        if isinstance(arg, dict):
            if platform_system in arg:
                args_pl += arg[platform_system]
        else:   args_pl.append(arg)
    return args_pl

def _path(args: List[str], base_dir=None) -> List[Path]:

    base_dir = Path('') if base_dir is None else base_dir
    return  [(base_dir/arg).absolute().as_posix() if isinstance(arg, (str, Path)) else arg for arg in args]

def _npath(args: List[str], base_dir=None) -> List[Path]:

    base_dir = Path('') if base_dir is None else base_dir
    return [os.path.normpath((base_dir/arg).as_posix()) if isinstance(arg, (str, Path)) else arg for arg in args]

def _tupl(args: List[List[str]]) -> List[Tuple[str, str]]:

    return  [tuple(arg) for arg in args]

def scan_ftypes(folder: Union[str, Path],   ftypes: List[str],
                only: str=None,             recursive: bool=True):

    matches = []
    if recursive:
        for root, dirs, files in os.walk(folder):
            root = Path(root).absolute()
            if only in (None, 'files'):
                matches+=                [str(root/f) for ftype in ftypes for f in files if f.endswith(ftype)]
            if only in (None, 'dirs'):
                matches+=                [str(root/d) for ftype in ftypes for d in dirs if d.endswith(ftype)]
    else:
        for file_or_dir in os.listdir(folder):
            f_obj = (Path(folder) / file_or_dir).absolute()
            if only in (None, 'files') and f_obj.is_file() and f_obj.suffix in ftypes:
                matches+= [str(f_obj)]
            if only in (None, 'dirs') and f_obj.is_dir() and                any([f_obj.name.endswith(ftype) for ftype in ftypes]):
                matches+= [str(f_obj)]
    return matches

def shutil_copy_same_ok(src_list: List[Union[str, Path]], dst: Union[str, Path]):

    if not Path(dst).exists() or not Path(dst).is_dir():
        Path(dst).mkdir(parents=True)
    for src in src_list:
        try:
            shutil.copy(src, dst)
        except shutil.SameFileError:
            pass


def run_command(command, **kwargs):

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        **kwargs,
    )
    while True:
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
        print(line.decode("utf-8", "backslashreplace"), end='')




from distutils.cmd import Command
class FlushCommand(Command):

    CLEAN_FILES = "*/__pycache__ .eggs ./gmon.out ./build ./.pytest_cache "                  "./dist ./*.pyc ./*.tgz ./*.egg-info Pyfhel/*.pyd coverage.xml ./htmlcov **/__pycache__ "                  "Pyfhel/*.lib Pyfhel/*.dll Pyfhel/*.exp .coverage".split(" ")
    CLEAN_GITIGNORES = ["Pyfhel/backend/SEAL"]
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        here = os.getcwd()
        for path_spec in self.CLEAN_FILES:

            abs_paths = glob.glob(os.path.normpath(os.path.join(here, path_spec)))
            for path in [str(p) for p in abs_paths]:
                if not path.startswith(here):

                    raise ValueError("%s is not a path inside %s" % (path, here))
                print('removing %s' % os.path.relpath(path))
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    shutil.rmtree(path)

        for git_repo in self.CLEAN_GITIGNORES:
            print('Emptying gitignored files in repo %s' % os.path.relpath(git_repo))
            run_command(['git', 'clean', '-dfX'], cwd=Path(git_repo).absolute())


















built_libs = {}


cpplibraries = []
for lib_name, lib_conf in config.pop('cpplibraries', {}).items():
    if lib_conf.get('mode') == 'cmake':
        cpplibraries.append(
            (lib_name,
            {'mode':                lib_conf.get('mode'),
            'lib_type':             lib_conf.get('lib_type', 'shared'),
            'source_dir':           Path(lib_conf.get('source_dir')).absolute(),
            'include_dirs':         _path(lib_conf.get('include_dirs', [])),
            'built_library_dir':    lib_conf.get('built_library_dir', 'lib'),
            'built_include_dirs':   lib_conf.get('built_include_dirs', []),
            'cmake_opts':           lib_conf.get('cmake_opts', {}),
            'sources':              [],
            })
        )
    else:
        cpplibraries.append(
            (lib_name,
            {'mode':                lib_conf.get('mode'),
            'lib_type':             lib_conf.get('lib_type', 'shared'),
            'sources':              _path(_pl(lib_conf.get('sources', []))),
            'include_dirs':         _path(_pl(lib_conf.get('include_dirs', []))),
            'extra_compile_args':   _pl(lib_conf.get('extra_compile_args',[])),
            'extra_link_args':      _pl(lib_conf.get('extra_link_args',[])),
            'macros':               _tupl(_pl(lib_conf.get('define_macros', []))),
            'libraries':            _pl(lib_conf.get('libraries', [])),
            'library_dirs':         _path(_pl(lib_conf.get('library_dirs', []))),
            })
        )


def _resolve_built_deps(lib_name: str, lib_conf: Dict) -> Tuple[str, Dict]:

    global built_libs
    for lib in lib_conf.get('libraries'):

        if built_libs.get(lib,{}).get('mode') == 'cmake':

            if lib_conf.get('lib_type')==built_libs[lib].get('lib_type')=='static':
                raise TypeError("Static (cmake-built) libs cannot be linked to other static libs")

            lib_conf['libraries'].remove(lib)
            lib_conf['libraries'].extend(built_libs[lib]['built_libraries'])


            lib_conf['include_dirs'].extend(built_libs[lib]['built_include_dirs'])
            lib_conf['include_dirs'].extend(built_libs[lib]['include_dirs'])


            lib_conf['library_dirs'].extend(list(set(
                [Path(l).parent.absolute().as_posix()                    for l in built_libs[lib]['built_lib_files']])))

        elif built_libs.get(lib,{}).get('mode') == 'standard':

            lib_conf['include_dirs'].extend(built_libs[lib]['include_dirs'])

    return lib_name, lib_conf


from setuptools.command.build_clib import build_clib
from distutils import log

class SuperBuildClib(build_clib):
    def finalize_options(self):
        build_clib.finalize_options(self)
        self.final_lib_folder = os.path.join(
            self.build_temp.replace("temp.", "lib."), project_name)

    def build_libraries(self, libraries):

        global built_libs


        self.cmake_libs =   [(l_name, b_info) for (l_name, b_info) in libraries                                if b_info.get('mode') == 'cmake']
        self.standard_libs =[(l_name, b_info) for (l_name, b_info) in libraries                                if b_info.get('mode') in ('standard', None)]


        for (lib_name, build_info) in self.cmake_libs:
            self.build_cmake_lib(lib_name, build_info)


        for (lib_name, build_info) in self.standard_libs:


            lib_name, build_info = _resolve_built_deps(lib_name, build_info)


            if build_info.get('lib_type')   == 'static':
                self.build_static_lib(lib_name, build_info)
            elif build_info.get('lib_type') == 'shared':
                self.build_shared_lib(lib_name, build_info)
            else:
                raise ValueError(f"Wrong {lib_name} library type {build_info.get('lib_type')}")



        for lib in built_libs:
            shutil_copy_same_ok(built_libs[lib]['built_lib_files'], self.final_lib_folder)
            shutil_copy_same_ok(built_libs[lib]['built_lib_files'], self.build_temp)


    def build_cmake_lib(self, lib_name, build_info, n_jobs=4):

        global built_libs

        log.info("building '%s' cmake-based library", lib_name)

        build_type = build_info.get('lib_type')
        build_dir = Path(self.build_clib).absolute() / project_name / lib_name
        build_dir.mkdir(parents=True, exist_ok=True)
        source_dir = build_info.get('source_dir')
        cmake_opts = build_info.get('cmake_opts')


        self.run_cmake_cli(source_dir, build_dir, cmake_opts)


        lib_dir = build_dir / build_info.get('built_library_dir')
        built_lib_files = list(lib_dir.rglob(f'*{get_lib_suffix(build_type)}'))
        lib_file_to_name =            lambda f: re.sub(f"{get_lib_prefix()}(.*){get_lib_suffix(build_type)}", r"\1", str(f))
        build_info.update({
            'built_lib_files': built_lib_files,
            'built_libraries': [lib_file_to_name(Path(f).name) for f in built_lib_files],
            'built_include_dirs':  _path(build_info.get('built_include_dirs'), base_dir=build_dir),
        })
        built_libs.update({lib_name: build_info})


    def build_static_lib(self, lib_name, build_info):

        global built_libs

        log.info("building '%s' static library", lib_name)

        sources = build_info.get('sources')
        expected_objects =            self.compiler.object_filenames(sources,output_dir=self.build_temp,)
        self.compiler.compile(
            sources             = sources,
            output_dir          = self.build_temp,
            macros              = build_info['macros'],
            include_dirs        = build_info['include_dirs'],
            extra_postargs      = build_info['extra_compile_args'],
            debug               = True
        )


        self.compiler.create_static_lib(
            expected_objects,
            lib_name,
            output_dir          = self.build_clib,
            libraries           = build_info['libraries'],
            library_dirs        = build_info['library_dirs'],
            extra_postargs      = build_info['extra_link_args'],
            debug               = True
        )

        lib_file = f"{get_lib_prefix()}{lib_name}{get_lib_suffix('static')}"
        build_info.update({
            'built_lib_files': [str(Path(self.build_clib).absolute() / lib_file)]
        })
        built_libs.update({lib_name: build_info})

    def build_shared_lib(self, lib_name, build_info):

        global built_libs
        log.info("building '%s' shared library", lib_name)







        if platform_system in ('Windows', 'Darwin'):
            if platform_system == 'Darwin':


                lib_file = f"{get_lib_prefix()}{lib_name}{get_lib_suffix('shared')}"
                install_name_flag = f"-Wl,-install_name,@loader_path/{lib_file}"
                if install_name_flag not in build_info['extra_link_args']:
                    build_info['extra_link_args'].append(install_name_flag)
            self.build_mocked_cmake_lib(lib_name, build_info)
            return

        sources = build_info.get('sources')
        objects = self.compiler.compile(
            sources             = sources,
            output_dir          = self.build_temp,
            macros              = build_info['macros'],
            include_dirs        = build_info['include_dirs'],
            extra_postargs      = build_info['extra_compile_args'],
            debug               = True
            )


        language = self.compiler.detect_language(sources)
        lib_file = f"{get_lib_prefix()}{lib_name}{get_lib_suffix('shared')}"

        if platform_system == 'Darwin':


            build_info['extra_link_args'].append(f"-Wl,-install_name,@loader_path/{lib_file}")
            try:
                self.compiler.linker_so = ['-dynamiclib' if val=='-bundle' else val for val in self.compiler.linker_so]
            except Exception:
                pass
        self.compiler.link_shared_object(
            objects,
            lib_file,
            output_dir          = self.build_clib,
            target_lang         = language,
            libraries           = build_info['libraries'],
            library_dirs        = build_info['library_dirs'],
            extra_postargs      = build_info['extra_link_args'],
            build_temp          = self.build_temp,
        )

        build_info.update({
            'built_lib_files': [str(Path(self.build_clib).absolute() / lib_file)]
        })
        built_libs.update({lib_name: build_info})

    def build_mocked_cmake_lib(self, lib_name, build_info):

        global built_libs



        build_dir = Path(self.build_temp).absolute() / project_name / f"cmake_{lib_name}"
        build_dir.mkdir(parents=True, exist_ok=True)
        source_dir = '.'

        with open(build_dir/"CMakeLists.txt", 'w') as f:
            f.write("cmake_minimum_required(VERSION 3.8)\n")
            f.write(f"project(mocked_cmake_shared_lib_{lib_name})\n")


            f.write("set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)\n")


            output_dir = Path(self.build_temp).absolute().as_posix()
            f.write(f"set(CMAKE_LIBRARY_OUTPUT_DIRECTORY \"$<1:{output_dir}>\")\n")
            f.write(f"set(CMAKE_RUNTIME_OUTPUT_DIRECTORY \"$<1:{output_dir}>\")\n")
            f.write(f"set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY \"$<1:{output_dir}>\")\n")


            extra_c_args = ' '.join(build_info['extra_compile_args'])
            if extra_c_args:
                f.write(f"add_compile_options({extra_c_args})\n")
            for d in build_info['include_dirs']:
                f.write(f"include_directories(\"{d}\")\n")
            macros = [f"-d{m[0]}={m[1]}" for m in build_info['macros']]
            if macros:
                f.write(f"add_compile_options({' '.join(macros)})\n")
            extra_l_args = ' '.join(build_info['extra_link_args'])
            if extra_l_args:
                f.write(f"add_link_options({extra_l_args})\n")
            lib_type = build_info['lib_type'].upper()
            sources = ' '.join([f'\"{s}\"' for s in build_info['sources']])
            f.write(f"add_library({lib_name} {lib_type} {sources})\n")
            lib_paths = ' '.join([f'\"{str(p)}\"' for p in build_info['library_dirs']])
            if build_info['libraries']:
                lib_cmake_var_names = [cmake_varify_lib_name(l)
                                  for l in build_info['libraries']]
                for l, lib_cmake_var in zip(build_info['libraries'], lib_cmake_var_names):

                    f.write(f"unset({lib_cmake_var} CACHE)\n")
                    f.write(f"find_library({lib_cmake_var} {l} PATHS {lib_paths} NO_DEFAULT_PATH REQUIRED)\n")
                lib_cmake_vars = ' '.join([f"${ {var}} " for var in lib_cmake_var_names])

                f.write(f"message(STATUS \"{lib_name}: link libs = {lib_cmake_vars}\")\n")
                f.write(f"target_link_libraries({lib_name} {lib_cmake_vars})\n")



        self.run_cmake_cli(source_dir, build_dir)


        lib_files = [lf.absolute() for lf in
                     Path(output_dir).glob(f'{get_lib_prefix()}{lib_name}*')]
        build_info.update({'built_lib_files': lib_files})
        built_libs.update({lib_name: build_info})

    def run_cmake_cli(self, source_dir, build_dir, cmake_opts={}, n_jobs=4):



        cmake_ver_str = subprocess.run(['cmake', '--version'],
                        check=True, capture_output=True, text=True).stdout
        cmake_ver = Version(re.search(r'version (\d+\.\d+\.\d+)', cmake_ver_str).group(1))

        cmake_cli_opts = []

        cc = os.environ.get("CC")
        cxx = os.environ.get("CXX")
        if cc:
            cmake_cli_opts.append(f"-DCMAKE_C_COMPILER={cc}")
        if cxx:
            cmake_cli_opts.append(f"-DCMAKE_CXX_COMPILER={cxx}")



        cmake_config = cmake_opts.pop('CMAKE_BUILD_TYPE', 'Release')
        for k, v in cmake_opts.items():
            cmake_cli_opts.append(f"-D{k}={v}")


        if cmake_ver >= Version('3.14'):
            run_command(['cmake', '-S', source_dir, '-B', build_dir] + cmake_cli_opts
            , cwd=build_dir)
        else:
            run_command(['cmake', source_dir] + cmake_cli_opts, cwd=build_dir)


        run_command(['cmake', '--build',  '.', '-j', str(n_jobs)] +                    (['--config', cmake_config] if platform_system=="Windows" else []), cwd=build_dir)


def get_lib_suffix(lib_type: str) -> str:
    if lib_type == 'static':
        if platform_system == 'Windows':
            return '.lib'
        else:
            return '.a'
    else:
        if platform_system == 'Windows':
            return '.dll'
        elif platform_system == 'Darwin':
            return '.dylib'
        else:
            return '.so'

def get_lib_prefix() ->str:
    return 'lib' if platform_system!='Windows' else ''

def cmake_varify_lib_name(filename: str) -> str:


    sub_table = {
        r'-': r'\_',
        r'\.': r'',
        r' ': r'',
        r' ': r'',
    }
    regex = re.compile("(%s)" % "|".join(map(re.escape, sub_table.keys())))


    regex.sub(lambda mo: sub_table[mo.string[mo.start():mo.end()]], filename)
    return filename.upper()


















from setuptools.command.build_ext import build_ext
class SuperBuildExt(build_ext):
    def finalize_options(self):
        build_ext.finalize_options(self)



        import numpy
        log.info("cimporting numpy version '%s'", numpy.__version__)


        global built_libs
        self.include_dirs += [numpy.get_include()] +            [d for conf in built_libs.values()                for d in conf['include_dirs']+conf.get('built_include_dirs',[])                if d is not None]

    def build_extensions(self):




        global built_libs
        libs = set(self.compiler.libraries)
        if platform_system == 'Windows':
            cmake_built_lib_names = set([os.path.splitext(l)[0] for (_, b_info)                in built_libs.items() for l in b_info.get('built_lib_files',[])])
        else:
            cmake_built_lib_names = set([l for (_, b_info) in built_libs.items()                for l in b_info.get('built_libraries',[]) if b_info.get('mode') == 'cmake'])
        cmake_lib_names = set([l_name for (l_name, b_info) in built_libs.items()            if b_info.get('mode') == 'cmake'])
        self.compiler.libraries = list(libs ^ cmake_lib_names | cmake_built_lib_names)
        build_ext.build_extensions(self)

    def copy_extensions_to_source(self):


        build_ext.copy_extensions_to_source(self)

        global built_libs
        package = '.'.join(self.get_ext_fullname(self.extensions[0].name).split('.')[:-1])
        package_dir = self.get_finalized_command('build_py').get_package_dir(package)
        for lib in self.libraries:
            shutil_copy_same_ok(built_libs[lib]['built_lib_files'], package_dir)




extensions          = config.pop('extensions', {})
config_all          = extensions.pop('config', {})

include_dirs        =  _path(_pl(config_all.get('include_dirs', [])))
define_macros       =  _tupl(_pl(config_all.get('define_macros', [])))
extra_compile_args  =  _pl(config_all.get('extra_compile_args', []))
extra_link_args     =  _pl(config_all.get('extra_link_args', []))
libraries           =  _pl(config_all.get('libraries', []))
library_dirs        =  _path(_pl(config_all.get('library_dirs', [])))


if COVERAGE:
    define_macros += [('CYTHON_TRACE', 1), ('CYTHON_TRACE_NOGIL', 1)]

ext_modules = []
for ext_name, ext_conf in extensions.items():
    ext_modules.append(Extension(
        name            = ext_conf.pop('fullname', f"{project_name}.{ext_name}"),
        sources         =_npath(_pl(ext_conf.pop('sources', []))),
        include_dirs    = _path(_pl(ext_conf.pop('include_dirs', [])))      + include_dirs,
        define_macros   = _tupl(_pl(ext_conf.pop('include_dirs', [])))      + define_macros,
        language        = "c++",
        extra_compile_args=     _pl(ext_conf.pop('extra_compile_args', [])) + extra_compile_args,
        extra_link_args =       _pl(ext_conf.pop('extra_link_args', []))    + extra_link_args,
        libraries       =       _pl(ext_conf.pop('libraries', []))          + libraries,
        library_dirs    = _path(_pl(ext_conf.pop('library_dirs', [])))      + library_dirs,
    ))



if CYTHONIZE:
    cython_directives = {
        'embedsignature': True,
        'language_level': 3,
        'cdivision': True,
        'boundscheck': False,
        'c_string_type': 'unicode',
        'c_string_encoding': 'ascii',
        'wraparound': False,
        'initializedcheck': False,
        'linetrace': COVERAGE,
    }
    ext_modules=cythonize(
        ext_modules,
        compiler_directives=cython_directives)

else:
    for ext in ext_modules:
        ext.sources = [s.replace(".pyx", ".cpp")            if Path(s.replace(".pyx", ".cpp")).exists() else s for s in ext.sources]






with open(project_config['readme'], "r") as f:
    long_description = f.read()

setup(

    name            = project_name,
    version         = VERSION,
    author          = ', '.join([n['name'] for n in project_config['authors']]),
    author_email    = ', '.join([n['email'] for n in project_config['authors']]),
    url             = project_config['urls']['documentation'],
    description     = project_config['description'],
    long_description= long_description,
    long_description_content_type="text/markdown",
    download_url    = project_config['urls']['repository'],
    classifiers     = project_config['classifiers'],
    platforms       = config['platforms']['platforms'],
    keywords        = ', '.join(project_config['description']),

    python_requires =project_config['requires-python'],
    zip_safe        =False,
    packages        =find_packages(),
    include_package_data=False,
    ext_modules     =ext_modules,
    libraries       =cpplibraries,
    cmdclass        ={'flush': FlushCommand,
                      'build_ext' : SuperBuildExt,
                      'build_clib' : SuperBuildClib},
)
