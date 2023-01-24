#include <cstdlib>
#include <iostream>
#include <string>

#include <CLI/CLI.hpp>

#include <boost/filesystem.hpp>

#include <boost/nowide/args.hpp>
#include <boost/nowide/cstdio.hpp>
#include <boost/nowide/filesystem.hpp>
#include <boost/nowide/fstream.hpp>
#include <boost/nowide/iostream.hpp>

#include <boost/dll/runtime_symbol_info.hpp>

#include <vulkan/vulkan.h>

#include <GLFW/glfw3.h>

namespace nowide {
using namespace boost::nowide;
};

int main(int argc, char *argv[]) {
    nowide::nowide_filesystem();

    CLI::App app{"CLI11应用"};
    std::string p = "调试";
    app.add_option("-p", p, "参数");

    nowide::args _(argc, argv);
    try {
        app.parse(argc, argv);
    } catch (const CLI::ParseError &e) {
        return app.exit(e, nowide::cout, nowide::cerr);
    }

    nowide::cout << "参数值： " << p << std::endl;
    nowide::cout << "测试" << '\n';
    FILE *f = nowide::fopen(p.c_str(), "w");
    std::fputs("测试测试", f);
    std::fclose(f);

    const auto exe_dir = boost::dll::program_location().parent_path();
    nowide::cout << exe_dir << '\n';

    return 0;
}
