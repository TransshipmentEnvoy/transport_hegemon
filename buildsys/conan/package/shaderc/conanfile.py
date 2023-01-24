import os

from conan import ConanFile
from conan.tools import build
from conan.tools import files
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout

import shutil


class ShadercConan(ConanFile):
    name = "shaderc"
    description = "A collection of tools, libraries and tests for shader compilation."
    license = "Apache-2.0"
    topics = ("conan", "shaderc", "glsl", "hlsl", "msl", "spirv", "spir-v", "glslc")
    url = "https://github.com/google/shaderc"
    exports_sources = ["CMakeLists.txt"]
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {"shared": False, "fPIC": True}

    def export_sources(self):
        patch_file_list = ["patch/fix-cmake.patch"]
        for patch_file in patch_file_list:
            src = os.path.join(self.recipe_folder, patch_file)
            dst = os.path.join(self.export_sources_folder, patch_file)
            files.mkdir(self, os.path.dirname(dst))
            shutil.copy2(src, dst)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)

    @property
    def _get_compatible_spirv_tools_version(self):
        return {
            "2022.4": "1.3.236.0",
        }.get(str(self.version), False)

    @property
    def _get_compatible_glslang_version(self):
        return {
            "2022.4": "1.3.236.0",
        }.get(str(self.version), False)

    def requirements(self):
        self.requires("glslang/{}".format(self._get_compatible_glslang_version))
        self.requires("spirv-tools/{}".format(self._get_compatible_spirv_tools_version))

    def validate(self):
        if self.info.settings.compiler.get_safe("cppstd"):
            build.check_min_cppstd(self, 11)

    def source(self):
        files.get(self, f"https://github.com/google/shaderc/archive/refs/tags/v{self.version}.tar.gz", strip_root=True)

        # apply patches
        files.patch(self, patch_file="patch/fix-cmake.patch")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.get_safe("fPIC", True)
        tc.variables["SHADERC_SKIP_INSTALL"] = False
        tc.variables["SHADERC_SKIP_TESTS"] = True
        tc.variables["SHADERC_ENABLE_WERROR_COMPILE"] = False
        if self.settings.compiler == "Visual Studio":
            tc.variables["SHADERC_ENABLE_SHARED_CRT"] = str(self.settings.compiler.runtime).startswith("MD")
        tc.variables["ENABLE_CODE_COVERAGE"] = False

        # dependencies (targets) should be included in patch (with CMakeDeps & find_package)
        tc.generate()

        cmake_deps = CMakeDeps(self)
        cmake_deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self.source_folder)
        cmake = CMake(self)
        cmake.install()
        files.rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        self.cpp_info.set_property("cmake_target_name", "shaderc" if self.options.shared else "shaderc_static")
        self.cpp_info.libs = self._get_ordered_libs()
        if self.settings.os == "Linux":
            self.cpp_info.system_libs.append("pthread")
        if not self.options.shared and build.stdcpp_library(self):
            self.cpp_info.system_libs.append(build.stdcpp_library(self))
        if self.options.shared:
            self.cpp_info.defines.append("SHADERC_SHAREDLIB")

        bin_path = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH environment variable: {}".format(bin_path))
        self.env_info.PATH.append(bin_path)

    def _get_ordered_libs(self):
        libs = ["shaderc_shared" if self.options.shared else "shaderc"]
        if not self.options.shared:
            libs.append("shaderc_util")

        return libs
