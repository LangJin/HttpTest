
# 安装allure工具
1、在powershell输入，安装scoop
>Set-ExecutionPolicy RemoteSigned -scope CurrentUser iex (new-object net.webclient).downloadstring('https://get.scoop.sh') 

2、安装allure
>scoop install allure 

3、配置java环境变量   
4、安装第三方包
>pip install allure-pytest   

5、编写代码  
6、本地执行并查看报告  
运行脚本并生成测试报告需要的文件 
>py.test --alluredir=%allure_result_folder% ./tests   

生成报告   
>allure serve %allure_result_folder%  
allure generate ./result/ -o ./report/ --clean     

打开报告   
>allure open -h 127.0.0.1 -p 8083 ./report/  


# 集成jenkins
1、下载安装jenkins  
2、安装allure插件  
3、新建job   1、打开代码所在路径   2、path result  
4、构建  

```py
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
```