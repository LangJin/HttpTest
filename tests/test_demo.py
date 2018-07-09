

'''

$ pip install allure-pytest 
$ py.test --alluredir=%allure_result_folder% ./tests 
$ allure serve %allure_result_folder%

py.test --alluredir ./test

安装命令行工具 首先需要安装命令行工具，如果是Mac电脑，推荐使用Homebrew安装。 $ brew install allure

生成测试报告 安装完成后，通过下面的命令将./result/目录下的测试数据生成测试报告： $ allure generate ./result/ -o ./report/ --clean 这样在./report/目录下就生成了Allure的测试报告了。–clean目的是先清空测试报告目录，再生成新的测试报告。

打开测试报告 
通过下面的命令打开测试报告： $ allure open -h 127.0.0.1 -p 8083 ./report/ 
本机的浏览器将打开http://127.0.0.1:8083/index.html网页，展示测试报告。

安装scopr 
Set-ExecutionPolicy RemoteSigned -scope CurrentUser iex (new-object net.webclient).downloadstring('https://get.scoop.sh') 
安装allure 
scoop install allure 
配置java环境变量 
安装
allure-pytest
运行脚本并生成测试报告需要的文件 py.test --alluredir=%allure_result_folder% ./tests 
生成报告 allure generate ./result/ -o ./report/ --clean 
打开报告 allure open -h 127.0.0.1 -p 8083 ./report/


集成jenkins
1、下载安装jenkins
2、安装allure插件
3、新建job   1、打开代码所在路径   2、path result
4、构建
'''
import allure

@allure.feature('testsuite1')
@allure.story('testcass1')
def test_minor():
    allure.environment(country='countrys')
    with allure.step("步骤一"):
        @allure.attach("说明这个步骤", "???")
        assert True
    with allure.step("步骤二", "???"):
        @allure.attach("说明")
        assert True
    with allure.step("步骤三", "???"):
        @allure.attach("说明")
        assert False


@allure.title("测试报告")
@allure.severity("critical")  # 优先级，包含blocker, critical, normal, minor, trivial 几个不同的等级
@allure.feature('testsuite2')
@allure.story('testcass2', 'testcass3')
@allure.story('testcass4')
class TestBar:
    def test_bar(self):
        @allure.attach("说明")
        assert True

    def test_bar2(self):
        with allure.step("步骤一"):
            @allure.attach("说明")
            assert True
        with allure.step("步骤二"):
            @allure.attach("说明")
            assert True
        with allure.step("步骤三"):
            @allure.attach("说明")
            assert True