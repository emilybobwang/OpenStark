# CRF框架函数大全
[TOC]
## Selenium相关(Core.Keywords.selenium)
### 浏览器管理
#### close_all_browsers
```
close_all_browsers()
    关闭所有浏览器并重置浏览器缓存
    参数: 无
    返回值: 无
```
#### close_browser
```
close_browser()
    关闭当前浏览器
    参数: 无
    返回值: 无
```
#### open_browser
```
open_browser(url, browser='firefox', alias=None, remote_url=False,
            desired_capabilities=None, ff_profile_dir=None)
    打开一个新浏览器实例并访问指定的URL
    参数: url                   要访问的链接
          browser               浏览器类型  
          alias                 别名
          remote_url            selenium远程服务器地址    
          desired_capabilities  指定selenium远程服务器地址后需要的表单字符串
          ff_profile_dir        Firefox的配置文件目录的路径
    返回值: 浏览器实例的索引
    browser参数可选的值如下:
    | firefox          | FireFox                            |
    | ff               | FireFox                            |
    | internetexplorer | Internet Explorer                  |
    | ie               | Internet Explorer                  |
    | googlechrome     | Google Chrome                      |
    | gc               | Google Chrome                      |
    | chrome           | Google Chrome                      |
    | opera            | Opera                              |
    | phantomjs        | PhantomJS                          |
    | htmlunit         | HTMLUnit                           |
    | htmlunitwithjs   | HTMLUnit with Javascipt support    |
    | android          | Android                            |
    | iphone           | Iphone                             |
    | safari           | Safari                             |
    | edge             | Edge                               |
```
#### create_webdriver
```
create_webdriver(driver_name, alias=None, kwargs={}, **init_kwargs)
    创建一个WebDriver的实例
    参数: driver_name  WebDriver的确切名称, 包括Firefox, Chrome, Ie, Opera, Safari, PhantomJS, Remote         
          alias        别名
          kwargs       传递给WebDriver的参数  
    返回值: 浏览器实例的索引
```
#### open_wdBrowser
```
open_wdBrowser(url, browser='Chrome')
    打开一个使用WebDriver创建的浏览器并访问指定的URL
    参数: url     要访问的链接   
          browser 浏览器类型, 可选Chrome, PhantomJS
    返回值: 浏览器实例的索引
```
#### switch_browser
```
switch_browser(index_or_alias)
    使用索引或别名切换在活动的浏览器
    参数: index_or_alias  索引或别名
    返回值: 无
```
#### close_window
```
close_window()
    关闭当前活动窗口
    参数: 无
    返回值: 无
```
#### get_window_identifiers
```
get_window_identifiers()
    返回并记录浏览器已知的所有窗口的属性。
    参数: 无
    返回值: 所有窗口的属性列表
```
#### get_window_names
```
get_window_names()
    返回并记录浏览器已知的所有窗口的名称
    参数: 无
    返回值: 所有窗口的名称列表
```
#### get_window_titles
```
get_window_titles()
    返回并记录浏览器已知的所有窗口的标题。
    参数: 无
    返回值: 所有窗口的标题列表
```
#### maximize_browser_window
```
maximize_browser_window()
    最大化当前窗口
    参数: 无
    返回值: 无
```
#### get_window_size
```
get_window_size()
    获取当前窗口的大小
    参数: 无
    返回值: 宽 高
```
#### set_window_size
```
set_window_size(width, height)
    设置当前窗口的大小
    参数: width   宽
          height  高
    返回值: 宽 高
```
#### get_window_position
```
get_window_position()
    获取当前窗口的坐标位置
    参数: 无
    返回值: 横坐标 纵坐标 
```
#### set_window_position
```
set_window_position(x, y)
    设置当前窗口的坐标位置
    参数: x   横坐标
          y   纵坐标
    返回值: 横坐标 纵坐标 
```
#### select_frame
```
select_frame(locator)
    将`locator`标识的frame设置为当前frame。
    参数: locator  frame的id、name或xpath
    返回值: 无
```
#### select_window
```
select_window(locator=None)
    选择`locator`标识的窗口并返回窗口句柄
    参数: locator  窗口的name, title, url, window handle
    返回值: 窗口句柄
```
#### get_log
```
get_log(log_type)
    获取指定selenium类型的日志
    参数:  log_type   selenium类型, 可选browser, driver, client或server
    返回值: 日志内容
```
#### list_windows
```
list_windows()
    返回当前所有窗口句柄
    参数: 无
    返回值: 所有窗口句柄列表
```
#### unselect_frame
```
unselect_frame()
    切换回默认frame窗口
    参数: 无
    返回值: 无
```
#### get_location
```
get_location()
    获取当前窗口的URL链接
    参数: 无
    返回值: URL
```
#### get_locations
```
get_locations()
    返回所有窗口的URL链接
    参数: 无
    返回值: URL链接列表
```
#### get_source
```
get_source()
    获取当前页面源码
    参数: 无
    返回值: 当前页面源码
```
#### get_title
```
get_title()
    获取当前页面标题
    参数: 无
    返回值: 当前页面标题
```
#### location_should_be
```
location_should_be(url)
    断言当前页面链接与给定的链接是否一致
    参数: url     指定链接
    返回值: 不符抛出异常
```
#### location_should_contain
```
location_should_contain(expected)
    断言当前页面链接是否包含指定内容
    参数: expected    预期检查内容
    返回值: 不符抛出异常
```
#### log_location
```
log_location()
    返回当前页面链接并打印日志
    参数: 无
    返回值: 当前页面链接
```
#### log_title
```
log_title()
    返回当前页面标题并打印日志
    参数: 无
    返回值: 当前页面标题
```
#### title_should_be
```
title_should_be(title)
    断言当前页面标题是否跟指定的标题一致
    参数: title    标题
    返回值: 不符抛出异常
```
#### go_back
```
go_back()
    模拟用户点击浏览器的返回按钮
    参数: 无
    返回值: 无
```
#### go_to
```
go_to(url)
    跳转页面到指定链接
    参数: url     要跳转的链接
    返回值: 无
```
#### get_selenium_speed
```
get_selenium_speed()
    获取selenium的执行速度
    参数: 无
    返回值: selenium的执行速度(秒)
```
#### get_selenium_timeout
```
get_selenium_timeout()
    获取selenium的执行超时时间
    参数: 无
    返回值: selenium的执行超时时间
```
#### get_selenium_implicit_wait
```
get_selenium_implicit_wait()
    获取selenium执行时的等待时间
    参数: 无
    返回值: selenium执行时的等待时间
```
#### set_selenium_speed
```
set_selenium_speed(seconds)
    设置selenium的执行速度
    参数: seconds     速度(秒)
    返回值: 原来的selenium执行速度
```
#### set_selenium_timeout
```
set_selenium_timeout(seconds)
    设置selenium的执行超时时间
    参数: seconds     超时时间(秒)
    返回值: 原来的selenium执行超时时间
```
#### set_selenium_implicit_wait
```
set_selenium_implicit_wait(seconds)
    设置selenium执行时的等待时间
    参数: seconds     等待时间(秒)
    返回值: 原来的selenium执行时的等待时间
```
#### set_browser_implicit_wait
```
set_browser_implicit_wait(seconds)
    设置当前浏览器的执行时的等待时间
    参数: seconds     等待时间(秒)
    返回值: 无
```
### 告警弹窗操作
#### input_text_into_prompt
```
input_text_into_prompt(text)
    向弹窗中输入指定内容
    参数: text    要输入的文本
    返回值: 无
```
#### alert_should_be_present
```
alert_should_be_present(text='')
    验证弹窗是否存在并解除
    参数: text    指定告警弹窗文本
    返回值: 无
```
#### choose_cancel_on_next_confirmation
```
choose_cancel_on_next_confirmation()
    在下次进行确认操作时选择取消
    参数: 无
    返回值: 无
```
#### choose_ok_on_next_confirmation
```
choose_ok_on_next_confirmation()
    在下次进行确认操作时选择确定
    参数: 无
    返回值: 无
```
#### confirm_action
```
confirm_action()
    取消当前显示的确认对话框并返回消息
    参数: 无
    返回值: 弹窗消息
```
#### get_alert_message
```
get_alert_message(dismiss=True)
    获取告警弹窗消息
    参数: dismiss    是否解除告警 
    返回值: 告警弹窗消息
```
#### dismiss_alert
```
dismiss_alert(accept=True)
    确认或解除告警
    参数: accept    是否确认告警
    返回值: True / False
```
### Cookie管理
#### delete_all_cookies
```
delete_all_cookies()
    删除所有Cookie
    参数: 无
    返回值: 无
```
#### delete_cookie
```
delete_cookie(name)
    删除指定Cookie
    参数: name    cookie名称
    返回值: 无
```
#### get_cookies
```
get_cookies()
    获取当前页面所有的cookies
    参数: 无
    返回值: 无
```
#### get_cookie_value
```
get_cookie_value(name)
    获取指定name的cookie值
    参数: name    cookie名称
    返回值: cookie值
```
#### add_cookie
```
add_cookie(name, value, path=None, domain=None, secure=None)
    新增cookie到当前会话
    参数: name     cookie名称
          value    cookie值
          path     path属性值
          domain   domain属性值
          secure   secure属性值
    返回值: 无
```
### 页面元素操作
#### get_webelement
```
get_webelement(locator)
    获取第一个匹配到的页面元素节点
    参数: locator     元素定位表达式
    返回值: 第一个匹配到的页面元素
    元素定位表达式格式如下:
    |Strategy    |Match based on                     |Example
    -------------------------------------------------------------------------
    |id          |Element id.                        |id:example
    |name        |name attribute.                    |name:example
    |identifier  |Either id or name.                 |identifier:example
    |class       |Element class.                     |class:example
    |tag         |Tag name.                          |tag:div
    |xpath       |XPath expression.                  |xpath://div[@id="example"]
    |css         |CSS selector.                      |css:div#example
    |dom         |DOM expression.                    |dom:document.images[5]
    |link        |Exact text a link has.             |link:The example
    |partial link|Partial link text.                 |partial link:he ex
    |sizzle      |Sizzle selector provided by jQuery.|sizzle:div.example
    |jquery      |Same as the above.                 |jquery:div.example
    |default     |Keyword specific default behavior. |default:example
```
#### get_webelements
```
get_webelements(locator)
    返回所有匹配的页面元素节点
    参数: locator     元素定位表达式
    返回值: 所有匹配的页面元素节点
```
#### current_frame_should_contain
```
current_frame_should_contain(text, loglevel='INFO')
    当前frame是否包含指定的文本内容
    参数: text      文本内容
          loglevel  日志级别
    返回值: 不符合抛出异常
```
#### current_frame_should_not_contain
```
current_frame_should_not_contain(text, loglevel='INFO')
    当前frame应该不包含指定的文本内容
    参数: text      文本内容
          loglevel  日志级别
    返回值: 不符合抛出异常
```
#### element_should_contain
```
element_should_contain(locator, expected, message='')
    验证`locator`确定的元素是否包含指定文本
    参数: locator     元素定位表达式
          expected    预期文本内容  
          message     异常时的说明  
    返回值: 不符合抛出异常
```
#### element_should_not_contain
```
element_should_not_contain(locator, expected, message='')
    验证`locator`确定的元素不包含指定文本
    参数: locator     元素定位表达式
          expected    预期文本内容  
          message     异常时的说明  
    返回值: 不符合抛出异常
```
#### frame_should_contain
```
frame_should_contain(locator, text, loglevel='INFO')
    验证`locator`确定的frame是否包含指定文本
    参数: locator     元素定位表达式
          text        指定文本内容  
          loglevel    日志级别
    返回值: 不符合抛出异常
```
#### page_should_contain
```
page_should_contain(text, loglevel='INFO')
    验证当前页面是否包含指定文本
    参数: text      指定文本内容 
          loglevel  日志级别
    返回值: 不符合抛出异常
```
#### page_should_contain_element
```
page_should_contain_element(locator, message='', loglevel='INFO')
    验证当前页面是否包含指定的元素
    参数: locator   指定元素
          message   异常时的说明 
          loglevel  日志级别
    返回值: 不符合抛出异常
```
#### locator_should_match_x_times
```
locator_should_match_x_times(locator, expected_locator_count, message='', loglevel='INFO')
    验证页面指定元素是否匹配了X次
    参数: locator                   指定元素    
          expected_locator_count    预期匹配次数
          message                   异常时的说明 
    返回值: 不符合抛出异常
```
#### page_should_not_contain
```
page_should_not_contain(text, loglevel='INFO')
    当前页面需要不包含指定的文本
    参数: text      指定文本内容 
          loglevel  日志级别
    返回值: 不符合抛出异常
```
#### page_should_not_contain_element
```
page_should_not_contain_element(locator, message='', loglevel='INFO')
    当前页面需要不包含指定的元素
    参数: locator   指定元素
          message   异常时的说明 
          loglevel  日志级别
    返回值: 不符合抛出异常
```
#### assign_id_to_element
```
assign_id_to_element(locator, id)
    为`locator`指定的元素分配一个临时id
    参数: locator   指定元素
          id        临时id名称
    返回值: 无
```
#### element_should_be_disabled
```
element_should_be_disabled(locator)
    指定的元素需要是禁用状态
    参数: locator   指定元素
    返回值: 不符合抛出异常
```
#### element_should_be_enabled
```
element_should_be_enabled( locator)
    指定的元素需要是可用状态
    参数: locator   指定元素
    返回值: 不符合抛出异常
```
#### element_should_be_focused
```
element_should_be_focused(locator)
    指定的元素需要是聚焦状态
    参数: locator   指定元素
    返回值: 不符合抛出异常
```
#### element_should_be_visible
```
element_should_be_visible(locator, message='')
    指定的元素需要是可视状态
    参数: locator   指定元素
          message   异常时的说明
    返回值: 不符合抛出异常
```
#### element_should_not_be_visible
```
element_should_not_be_visible(locator, message='')
    指定的元素需要是不可视状态
    参数: locator   指定元素
          message   异常时的说明
    返回值: 不符合抛出异常
```
#### element_text_should_be
```
element_text_should_be(locator, expected, message='')
    指定元素节点文本需要与指定的文本相同
    参数: locator   指定元素
          expected  预期文本内容
          message   异常时的说明
    返回值: 不符合抛出异常
```
#### get_element_attribute
```
get_element_attribute(locator, attribute_name=None)
    获取节点元素的属性值
    参数: locator         指定元素
          attribute_name  需要获取的属性名称
    返回值: 属性值
```
#### get_horizontal_position
```
get_horizontal_position(locator)
    获取指定元素相对当前页面的横坐标
    参数: locator         指定元素
    返回值: 相对当前页面的横坐标
```
#### get_element_size
```
get_element_size(locator)
    获取指定元素的尺寸
    参数: locator         指定元素
    返回值: 指定元素的宽和高
```
#### get_value
```
get_value(locator)
    获取指定元素的value属性值
    参数: locator         指定元素
    返回值: value值
```
#### get_text
```
get_text(locator)
    获取指定元素的文本内容
    参数: locator         指定元素
    返回值: 文本值
```
#### clear_element_text
```
clear_element_text(locator)
    清除指定元素的文本内容
    参数: locator         指定元素
    返回值: 无
```
#### get_vertical_position
```
get_vertical_position(locator)
    获取指定元素相对当前页面的纵坐标
    参数: locator         指定元素
    返回值: 相对当前页面的纵坐标
```
#### click_element
```
click_element(locator)
    单击指定元素
    参数: locator         指定元素
    返回值: 无
```
#### click_element_at_coordinates
```
click_element_at_coordinates(locator, xoffset, yoffset)
    在元素指定的位置单击
    参数: locator         指定元素
          xoffset         横坐标
          yoffset         纵坐标
    返回值: 无
```
#### double_click_element
```
double_click_element(locator)
    双击指定元素
    参数: locator         指定元素
    返回值: 无
```
#### set_focus_to_element
```
set_focus_to_element(locator)
    聚焦到指定的元素
    参数: locator         指定元素
    返回值: 无
```
#### drag_and_drop
```
drag_and_drop(source, target)
    拖拽指定元素到指定目标元素之上
    参数: source    源元素
          target    目标元素
    返回值: 无
```
#### drag_and_drop_by_offset
```
drag_and_drop_by_offset(source, xoffset, yoffset)
    拖拽指定元素到指定坐标(相对当前位置)
    参数: source    源元素
          xoffset   偏移横坐标
          yoffset   偏移纵坐标
    返回值: 无
```
#### mouse_down
```
mouse_down(locator)
    模拟按住鼠标左键
    参数: locator         指定元素
    返回值: 无
```
#### mouse_out
```
mouse_out(locator)
    模拟鼠标离开指定元素
    参数: locator         指定元素
    返回值: 无
```
#### mouse_over
```
mouse_over(locator)
    模拟鼠标悬停在指定元素上方
    参数: locator         指定元素
    返回值: 无
```
#### mouse_up
```
mouse_up(locator)
    模拟释放鼠标左键
    参数: locator         指定元素
    返回值: 无
```
#### open_context_menu
```
open_context_menu(locator)
    在指定元素上打开右键菜单
    参数: locator         指定元素
    返回值: 无
```
#### simulate_event
```
simulate_event(locator, event)
    在指定的元素上模拟事件
    参数: locator   指定元素
          event     需要模拟的事件    
    返回值: 无
```
#### press_key
```
press_key(locator, key)
    在指定的元素上模拟键盘输入
    参数: locator   指定元素
          key       字符, 字符串或'\\\\'开头数字的ASCII码 
    返回值: 无
```
#### click_link
```
click_link(locator)
    单击指定链接
    参数: locator   指定元素
    返回值: 无
```
#### mouse_down_on_link
```
mouse_down_on_link(locator)
    在指定链接上模拟按住鼠标左键
    参数: locator   指定元素
    返回值: 无
```
#### page_should_contain_link
```
page_should_contain_link(locator, message='', loglevel='INFO')
    当前页面需要存在指定的链接
    参数: locator   指定元素
          message   异常时的说明
          loglevel  日志级别
    返回值: 不符合抛出异常
```
#### page_should_not_contain_link
```
page_should_not_contain_link(locator, message='', loglevel='INFO')
    当前页面不需要存在指定的链接
    参数: locator   指定元素
          message   异常时的说明
          loglevel  日志级别
    返回值: 不符合抛出异常
```
#### click_image
```
click_image(locator)
    单击指定图片
    参数: locator   指定元素
    返回值: 无
```
#### mouse_down_on_image
```
mouse_down_on_image(locator)
    在指定图片上模拟按住鼠标左键
    参数: locator   指定元素
    返回值: 无
```
#### page_should_contain_image
```
page_should_contain_image(locator, message='', loglevel='INFO')
    当前页面需要存在指定的图片
    参数: locator   指定元素
          message   异常时的说明
          loglevel  日志级别
    返回值: 不符合抛出异常
```
#### page_should_not_contain_image
```
page_should_not_contain_image(locator, message='', loglevel='INFO')
    当前页面需要不存在指定的图片
    参数: locator   指定元素
          message   异常时的说明
          loglevel  日志级别
    返回值: 不符合抛出异常
```
#### get_matching_xpath_count
```
get_matching_xpath_count(xpath, return_str=True)
    获取匹配指定xpath的次数
    参数: xpath         xpath表达式  
          return_str    是否返回字符串
    返回值: 匹配xpath的次数
```
#### xpath_should_match_x_times
```
xpath_should_match_x_times(xpath, expected_xpath_count, message='', loglevel='INFO')
    指定xpath需要匹配X次
    参数: xpath                 xpath表达式 
          expected_xpath_count  预期匹配次数
          message               异常时的说明
    返回值: 不符合抛出异常
```
#### add_location_strategy
```
add_location_strategy(strategy_name, strategy_keyword, persist=False)
    在关键字上添加自定义位置策略
    参数: strategy_name       策略名称
          strategy_keyword    策略关键字
          persist             是否全局注册
    返回值: 无
```
#### remove_location_strategy
```
remove_location_strategy(strategy_name)
    移除在关键字上添加的自定义位置策略
    参数: strategy_name       策略名称
    返回值: 无
```
### 表单操作
#### submit_form
```
submit_form(locator=None)
    提交表单
    参数: locator     表单元素标识
    返回值: 无
```
#### checkbox_should_be_selected
```
checkbox_should_be_selected(locator)
    验证checkbox是选中状态
    参数: locator     checkbox元素定位器              
    返回值: 不符合抛出异常
```
#### checkbox_should_not_be_selected
```
checkbox_should_not_be_selected(locator)
    验证checkbox是非选中状态
    参数: locator     checkbox元素定位器
    返回值: 不符合抛出异常
```
#### page_should_contain_checkbox
```
page_should_contain_checkbox(locator, message='', loglevel='INFO')
    验证当前页面是否存在指定checkbox
    参数: locator   checkbox元素定位器
          message   异常时的说明
          loglevel  日志级别
    返回值: 不符合抛出异常
```
#### page_should_not_contain_checkbox
```
page_should_not_contain_checkbox(locator, message='', loglevel='INFO')
    当前页面需要不存在指定checkbox
    参数: locator   checkbox元素定位器
          message   异常时的说明
          loglevel  日志级别
    返回值: 不符合抛出异常
```
#### select_checkbox
```
select_checkbox(locator)
    选中checkbox
    参数: locator   checkbox元素定位器
    返回值: 无
```
#### unselect_checkbox
```
unselect_checkbox(locator)
    取消选中checkbox
    参数: locator   checkbox元素定位器
    返回值: 无
```
#### page_should_contain_radio_button
```
page_should_contain_radio_button(locator, message='', loglevel='INFO')
    验证当前页面是否存在指定radio button
    参数: locator   radio button元素定位器
          message   异常时的说明
          loglevel  日志级别
    返回值: 不符合抛出异常
```
#### page_should_not_contain_radio_button
```
page_should_not_contain_radio_button(locator, message='', loglevel='INFO')
    当前页面需要不存在指定radio button
    参数: locator   radio button元素定位器
          message   异常时的说明
          loglevel  日志级别
    返回值: 不符合抛出异常
```
#### radio_button_should_be_set_to
```
radio_button_should_be_set_to(group_name, value)
    验证指定radio button是否被设置为指定的值
    参数: group_name   radio button name
          value        radio button value
    返回值: 不符合抛出异常
```
#### radio_button_should_not_be_selected
```
radio_button_should_not_be_selected(group_name)
    radio button需要不被选中
    参数: group_name   radio button name
    返回值: 不符合抛出异常
```
#### select_radio_button
```
select_radio_button(group_name, value)
    选中name=group_name和指定value的radio button
    参数: group_name   radio button name
          value        radio button value
    返回值: 无
```
#### choose_file
```
choose_file(locator, file_path)
    选中上传文件
    参数: locator       上传文本框定位器
          file_path     需要上传的文件路径
    返回值: 无
```
#### input_password
```
input_password(locator, text)
    输入密码
    参数: locator     文件框定位器
          text        密码字符串  
    返回值: 无
```
#### input_text
```
input_text(locator, text)
    输入文本
    参数: locator     文件框定位器
          text        文本 
    返回值: 无
```
#### page_should_contain_textfield
```
page_should_contain_textfield(locator, message='', loglevel='INFO')
    验证当前页面是否存在指定的textfield
    参数: locator   textfield元素定位器
          message   异常时的说明
          loglevel  日志级别
    返回值: 不符合抛出异常
```
#### page_should_not_contain_textfield
```
page_should_not_contain_textfield(locator, message='', loglevel='INFO')
    当前页面需要不存在指定的textfield
    参数: locator   textfield元素定位器
          message   异常时的说明
          loglevel  日志级别
    返回值: 不符合抛出异常
```
#### textfield_should_contain
```
textfield_should_contain(locator, expected, message='')
    验证textfield是否包含预期的内容
    参数: locator   textfield元素定位器
          expected  预期检查的内容
          message   异常时的说明
    返回值: 不符合抛出异常
```
#### textfield_value_should_be
```
textfield_value_should_be(locator, expected, message='')
    验证textfield是否等于预期的内容
    参数: locator   textfield元素定位器
          expected  预期检查的内容
          message   异常时的说明
    返回值: 不符合抛出异常
```
#### textarea_should_contain
```
textarea_should_contain(locator, expected, message='')
    验证textarea是否包含预期的内容
    参数: locator   textarea元素定位器
          expected  预期检查的内容
          message   异常时的说明
    返回值: 不符合抛出异常
```
#### textarea_value_should_be
```
textarea_value_should_be(locator, expected, message='')
    验证textarea是否等于预期的内容
    参数: locator   textarea元素定位器
          expected  预期检查的内容
          message   异常时的说明
    返回值: 不符合抛出异常
```
#### click_button
```
click_button(locator)
    单击button按钮
    参数: locator     button元素定位器
    返回值: 无
```
#### page_should_contain_button
```
page_should_contain_button(locator, message='', loglevel='INFO')
    验证当前页面是否包含指定button按钮
    参数: locator   button按钮元素定位器
          message   异常时的说明
          loglevel  日志级别
    返回值: 不符合抛出异常
```
#### page_should_not_contain_button
```
page_should_not_contain_button(locator, message='', loglevel='INFO')
    当前页面需要不包含指定button按钮
    参数: locator   button按钮元素定位器
          message   异常时的说明
          loglevel  日志级别
    返回值: 不符合抛出异常
```
### JavaScript相关
#### execute_javascript
```
execute_javascript(*code)
    执行javascript
    参数: code     javascript代码
    返回值: javascript执行结果
```
#### execute_async_javascript
```
execute_async_javascript(*code)
    异步执行javascript
    参数: code     javascript代码
    返回值: javascript执行结果
```
### 截屏操作
#### set_screenshot_directory
```
set_screenshot_directory(path, persist=False)
    配置截屏保存目录
    参数: path     截屏保存目录
          persist  是否全局注册 
    返回值: 无
```
#### capture_page_screenshot
```
capture_page_screenshot(filename='selenium-screenshot-{index}.png')
    截屏
    参数: filename    截屏保存文件名
    返回值: 截屏保存文件路径
```
### select相关操作
#### get_list_items
```
get_list_items(locator, value=False)
    返回指定元素选择器的标签列表或value值列表
    参数: locator     元素定位表达式
          value       是否返回value值
    返回值: 标签列表或value值列表
```
#### get_selected_list_label
```
get_selected_list_label(locator)
    返回选中状态的select list标签内容
    参数: locator     元素定位表达式
    返回值: select list标签内容
```
#### get_selected_list_labels
```
get_selected_list_labels(locator)
    返回选中状态的select list标签内容列表
    参数: locator     元素定位表达式
    返回值: select list标签内容列表
```
#### get_selected_list_value
```
get_selected_list_value(locator)
    返回选中状态的select list标签的value值
    参数: locator     元素定位表达式
    返回值: select list标签的value值
```
#### get_selected_list_values
```
get_selected_list_values(locator)
    返回选中状态的select list标签的value值列表
    参数: locator     元素定位表达式
    返回值: select list标签的value值列表
```
#### list_selection_should_be
```
list_selection_should_be(locator, *items)
    验证指定的select list与预期的是否一致
    参数: locator     元素定位表达式
          items       预期内容
    返回值: 不符合抛出异常
```
#### list_should_have_no_selections
```
list_should_have_no_selections(locator)
    验证指定的select list没有选中内容
    参数: locator     元素定位表达式
    返回值: 不符合抛出异常
```
#### page_should_contain_list
```
page_should_contain_list(locator, message='', loglevel='INFO')
    验证当前页面是否包含指定的select list
    参数: locator   元素定位表达式
          message   异常时的说明
          loglevel  日志级别
    返回值: 不符合抛出异常
```
#### page_should_not_contain_list
```
page_should_not_contain_list(locator, message='', loglevel='INFO')
    当前页面需要不包含指定的select list
    参数: locator   元素定位表达式
          message   异常时的说明
          loglevel  日志级别
    返回值: 不符合抛出异常
```
#### select_all_from_list
```
select_all_from_list(locator)
    选中指定多选列表框的所有值
    参数: locator   元素定位表达式
    返回值: 无
```
#### select_from_list
```
select_from_list(locator, *items)
    选中指定多选列表框的指定值
    参数: locator   元素定位表达式
          items     需要选择的值
    返回值: 无
```
#### select_from_list_by_index
```
select_from_list_by_index(locator, *indexes)
    根据索引选择列表
    参数: locator   元素定位表达式
          indexes   索引
    返回值: 无
```
#### select_from_list_by_value
```
select_from_list_by_value(locator, *values)
    根据value值选择列表
    参数: locator   元素定位表达式
          values    value值
    返回值: 无
```
#### select_from_list_by_label
```
select_from_list_by_label(locator, *labels)
    根据标签选择列表
    参数: locator   元素定位表达式
          labels    标签
    返回值: 无
```
#### unselect_from_list
```
unselect_from_list(locator, *items)
    取消选择列表的指定内容
    参数: locator   元素定位表达式
          items     取消选择的内容
    返回值: 无
```
#### unselect_from_list_by_index
```
unselect_from_list_by_index(locator, *indexes)
    根据索引取消选择列表
    参数: locator   元素定位表达式
          indexes   索引
    返回值: 无
```
#### unselect_from_list_by_value
```
unselect_from_list_by_value(locator, *values)
    根据value值取消选择列表
    参数: locator   元素定位表达式
          values    value值
    返回值: 无
```
#### unselect_from_list_by_label
```
unselect_from_list_by_label(locator, *labels)
    根据标签取消选择列表
    参数: locator   元素定位表达式
          labels    标签
    返回值: 无
```
### 表格相关操作
#### get_table_cell
```
get_table_cell(table_locator, row, column, loglevel='INFO')
    获取单元格内容
    参数: table_locator    表格元素定位表达式
          row              行
          column           列
          loglevel         日志级别
    返回值: 单元格内容
```
#### table_cell_should_contain
```
table_cell_should_contain(table_locator, row, column, expected, loglevel='INFO')
    验证指定单元格是否包含预期内容
    参数: table_locator    表格元素定位表达式
          row              行
          column           列
          expected         预期内容
          loglevel         日志级别
    返回值: 不符合抛出异常
```
#### table_column_should_contain
```
table_column_should_contain(table_locator, col, expected, loglevel='INFO')
    验证指定列是否包含预期内容
    参数: table_locator    表格元素定位表达式
          col              列
          expected         预期内容
          loglevel         日志级别
    返回值: 不符合抛出异常
```
#### table_footer_should_contain
```
table_footer_should_contain(table_locator, expected, loglevel='INFO')
    验证表格页脚是否包含预期内容
    参数: table_locator    表格元素定位表达式
          expected         预期内容
          loglevel         日志级别
    返回值: 不符合抛出异常
```
#### table_header_should_contain
```
table_header_should_contain(table_locator, expected, loglevel='INFO')
    验证表头是否包含预期内容
    参数: table_locator    表格元素定位表达式
          expected         预期内容
          loglevel         日志级别
    返回值: 不符合抛出异常
```
#### table_row_should_contain
```
table_row_should_contain(table_locator, row, expected, loglevel='INFO')
    验证指定行是否包含预期内容
    参数: table_locator    表格元素定位表达式
          row              行
          expected         预期内容
          loglevel         日志级别
    返回值: 不符合抛出异常
```
#### table_should_contain
```
table_should_contain(table_locator, expected, loglevel='INFO')
    验证表格是否包含预期内容
    参数: table_locator    表格元素定位表达式
          expected         预期内容
          loglevel         日志级别
    返回值: 不符合抛出异常
```
### 等待相关操作
#### wait_for_condition
```
wait_for_condition(condition, timeout=None, error=None)
    等待指定表达式为真
    参数: condition   JavaScript表达式
          timeout     超时时间
          error       出错时的提示信息
    返回值: 无
```
#### wait_until_page_contains
```
wait_until_page_contains(text, timeout=None, error=None)
    等待页面出现指定内容
    参数: text        指定文本内容
          timeout     超时时间
          error       出错时的提示信息
    返回值: 无
```
#### wait_until_page_does_not_contain
```
wait_until_page_does_not_contain(text, timeout=None, error=None)
    等待指定内容从当前页面消失
    参数: text        指定文本内容
          timeout     超时时间
          error       出错时的提示信息
    返回值: 无
```
#### wait_until_page_contains_element
```
wait_until_page_contains_element(locator, timeout=None, error=None)
    等待指定元素出现在当前页面
    参数: locator     指定元素
          timeout     超时时间
          error       出错时的提示信息
    返回值: 无
```
#### wait_until_page_does_not_contain_element
```
wait_until_page_does_not_contain_element(locator, timeout=None, error=None)
    等待指定元素从当前页面消失
    参数: locator     指定元素
          timeout     超时时间
          error       出错时的提示信息
    返回值: 无
```
#### wait_until_element_is_visible
```
wait_until_element_is_visible(locator, timeout=None, error=None)
    等待指定元素为可见状态
    参数: locator     指定元素
          timeout     超时时间
          error       出错时的提示信息
    返回值: 无
```
#### wait_until_element_is_not_visible
```
wait_until_element_is_not_visible(locator, timeout=None, error=None)
    等待指定元素为不可见状态
    参数: locator     指定元素
          timeout     超时时间
          error       出错时的提示信息
    返回值: 无
```
#### wait_until_element_is_enabled
```
wait_until_element_is_enabled(locator, timeout=None, error=None)
    等待指定元素为不可用状态
    参数: locator     指定元素
          timeout     超时时间
          error       出错时的提示信息
    返回值: 无
```
#### wait_until_element_contains
```
wait_until_element_contains(locator, text, timeout=None, error=None)
    等待指定元素包含预期内容
    参数: locator     指定元素
          text        预期内容
          timeout     超时时间
          error       出错时的提示信息
    返回值: 无
```
#### wait_until_element_does_not_contain
```
wait_until_element_does_not_contain(locator, text, timeout=None, error=None)
    等待指定元素不包含预期内容
    参数: locator     指定元素
          text        预期内容
          timeout     超时时间
          error       出错时的提示信息
    返回值: 无
```
##接口请求相关(Core.Keywords.requests)
#### create_session
```
create_session(alias, url, headers={}, cookies=None,
               auth=None, timeout=None, proxies=None,
               verify=False, debug=0, max_retries=3, backoff_factor=0.10, disable_warnings=0):
```
#### create_ntlm_session
```
create_ntlm_session(
            alias,
            url,
            auth,
            headers={},
            cookies=None,
            timeout=None,
            proxies=None,
            verify=False,
            debug=0,
            max_retries=3,
            backoff_factor=0.10,
            disable_warnings=0)
```
#### create_digest_session
```
create_digest_session(alias, url, auth, headers={}, cookies=None,
                      timeout=None, proxies=None, verify=False,
                      debug=0, max_retries=3,backoff_factor=0.10, disable_warnings=0):
```
#### delete_all_sessions
```
delete_all_sessions()
```
#### to_json
```
to_json(content, pretty_print=False)
```
#### get_request
```
get_request(
            alias,
            uri,
            headers=None,
            params=None,
            allow_redirects=None,
            timeout=None)
```
#### post_request
```
post_request(
            alias,
            uri,
            data=None,
            params=None,
            headers=None,
            files=None,
            allow_redirects=None,
            timeout=None)
```
#### patch_request
```
patch_request(
            alias,
            uri,
            data=None,
            params=None,
            headers=None,
            files=None,
            allow_redirects=None,
            timeout=None)
```
#### put_request
```
put_request(
            alias,
            uri,
            data=None,
            params=None,
            files=None,
            headers=None,
            allow_redirects=None,
            timeout=None)
```
#### delete_request
```
delete_request(
            alias,
            uri,
            data=(),
            params=None,
            headers=None,
            allow_redirects=None,
            timeout=None)
```
#### head_request
```
head_request(
            alias,
            uri,
            headers=None,
            allow_redirects=None,
            timeout=None)
```
#### options_request
```
options_request(
            alias,
            uri,
            headers=None,
            allow_redirects=None,
            timeout=None)
```
## 数据库操作相关(Core.Keywords.database)
#### connect_to_database
```
connect_to_database(dbapiModuleName=None, dbName=None, dbUsername=None, dbPassword=None, dbHost=None, dbPort=None, dbConfigFile="./resources/db.cfg"):
```
#### connect_to_database_using_custom_params
```
connect_to_database_using_custom_params(dbapiModuleName=None, db_connect_string=''):
```
#### disconnect_from_database
```
disconnect_from_database()
```
#### query
```
query(selectStatement)
```
#### row_count
```
row_count(selectStatement)
```
#### description
```
description(selectStatement)
```
#### delete_all_rows_from_table
```
delete_all_rows_from_table(tableName)
```
#### execute_sql_script
```
execute_sql_script(sqlScriptFileName)
```
#### execute_sql_string
```
execute_sql_string(sqlString)
```
#### check_if_exists_in_database
```
check_if_exists_in_database(selectStatement)
```
#### check_if_not_exists_in_database
```
check_if_not_exists_in_database(selectStatement)
```
#### row_count_is_0
```
row_count_is_0(selectStatement)
```
#### row_count_is_equal_to_x
```
row_count_is_equal_to_x(selectStatement,numRows)
```
#### row_count_is_greater_than_x
```
row_count_is_greater_than_x(selectStatement,numRows)
```
#### row_count_is_less_than_x
```
row_count_is_less_than_x(selectStatement,numRows)
```
#### table_must_exist
```
table_must_exist(tableName)
```
## QT测试数据生成器(Core.Keywords.qt)
#### count
```
count()
```
#### clear_counter
```
clear_counter()
```
#### gen_nums
```
gen_nums(counts)
```
#### gen_chars
```
gen_chars(counts, upper='M')
```
#### gen_birthday
```
gen_birthday(maxAge=55, minAge=21, sep='')
```
#### gen_idcard
```
gen_idcard(idcard='', maxAge=55, minAge=21)
```
#### gen_orgno
```
gen_orgno(orgno='', line=None)
```
#### gen_name
```
gen_name(num=3)
```
#### verify_idcard
```
verify_idcard(idcard)
```
#### verify_orgno
```
verify_orgno(orgno)
```
#### create_pboc
```
create_pboc(new_name, new_id, filepath)
```
## 文件对比(Core.Keywords.diff)
#### diff_files
```
diff_files(file1, file2, fail=True)
```
#### diff_outputs
```
diff_outputs(text1, text2, fail=True)
```
## 解压缩文件(Core.Keywords.archive)
#### extract_zip_file
```
extract_zip_file(zfile, dest=None)
```
#### extract_tar_file
```
extract_tar_file(tfile, dest=None)
```
#### archive_should_contain_file
```
archive_should_contain_file(zfile, filename)
```
#### create_tar_from_files_in_directory
```
create_tar_from_files_in_directory(directory, filename, sub_directories=True)
```
#### create_zip_from_files_in_directory
```
create_zip_from_files_in_directory(directory, filename, sub_directories=False)
```
## Appium相关(Core.Keywords.appium)
#### get_network_connection_status
```
get_network_connection_status()
```
#### set_network_connection_status
```
set_network_connection_status(connectionStatus)
```
#### pull_file
```
pull_file(path, decode=False)
```
#### pull_folder
```
pull_folder(path, decode=False)
```
#### push_file
```
push_file(path, data, encode=False)
```
#### get_activity
```
get_activity()
```
#### start_activity
```
start_activity(appPackage, appActivity, **opts)
```
#### wait_activity
```
wait_activity(activity, timeout, interval=1)
```
#### install_app
```
install_app(app_path, app_package)
```
#### press_keycode
```
press_keycode(keycode, metastate=None)
```
#### long_press_keycode
```
long_press_keycode(keycode, metastate=None)
```
#### zoom
```
zoom(locator, percent="200%", steps=1)
```
#### pinch
```
pinch(locator, percent="200%", steps=1)
```
#### swipe
```
swipe(start_x, start_y, offset_x, offset_y, duration=1000)
```
#### swipe_by_percent
```
swipe_by_percent(start_x, start_y, end_x, end_y, duration=1000)
```
#### scroll
```
scroll(start_locator, end_locator)
```
#### scroll_down
```
scroll_down(locator)
```
#### scroll_up
```
scroll_up(locator)
```
#### long_press
```
long_press(locator)
```
#### tap
```
tap(locator, x_offset=None, y_offset=None, count=1)
```
#### click_a_point
```
click_a_point(x=0, y=0, duration=100)
```
#### click_element_at_coordinates
```
click_element_at_coordinates(coordinate_X, coordinate_Y)
```
#### wait_until_element_is_visible
```
wait_until_element_is_visible(locator, timeout=None, error=None)
```
#### wait_until_page_contains
```
wait_until_page_contains(text, timeout=None, error=None)
```
#### wait_until_page_does_not_contain
```
wait_until_page_does_not_contain(text, timeout=None, error=None)
```
#### wait_until_page_contains_element
```
wait_until_page_contains_element(locator, timeout=None, error=None)
```
#### wait_until_page_does_not_contain_element
```
wait_until_page_does_not_contain_element(locator, timeout=None, error=None)
```
#### close_application
```
close_application()
```
#### close_all_applications
```
close_all_applications()
```
#### open_application
```
open_application( remote_url, alias=None, **kwargs)
```
#### switch_application
```
switch_application(index_or_alias)
```
#### reset_application
```
reset_application()
```
#### remove_application
```
remove_application(application_id)
```
#### get_appium_timeout
```
get_appium_timeout()
```
#### set_appium_timeout
```
set_appium_timeout(seconds)
```
#### get_appium_sessionId
```
get_appium_sessionId()
```
#### get_source
```
get_source()
```
#### log_source
```
log_source(loglevel='INFO')
```
#### go_back
```
go_back()
```
#### lock
```
lock(seconds=5)
```
#### background_app
```
background_app(seconds=5)
```
#### shake
```
shake()
```
#### portrait
```
portrait()
```
#### landscape
```
landscape()
```
#### get_current_context
```
get_current_context()
```
#### get_contexts
```
get_contexts()
```
#### get_window_height
```
get_window_height()
```
#### get_window_width
```
get_window_width()
```
#### switch_to_context
```
switch_to_context(context_name)
```
#### go_to_url
```
go_to_url(url)
```
#### get_capability
```
get_capability(capability_name)
```
#### capture_page_screenshot
```
capture_page_screenshot(filename=None)
```
#### clear_text
```
clear_text(locator)
```
#### click_element
```
click_element(locator)
```
#### click_button
```
click_button(index_or_name)
```
#### click_text
```
click_text(text, exact_match=False)
```
#### input_text
```
input_text(locator, text)
```
#### input_password
```
input_password(locator, text)
```
#### input_value
```
input_value(locator, text)
```
#### hide_keyboard
```
hide_keyboard(key_name=None)
```
#### page_should_contain_text
```
page_should_contain_text(text, loglevel='INFO')
```
#### page_should_not_contain_text
```
page_should_not_contain_text(text, loglevel='INFO')
```
#### page_should_contain_element
```
page_should_contain_element(locator, loglevel='INFO')
```
#### page_should_not_contain_element
```
page_should_not_contain_element(locator, loglevel='INFO')
```
#### element_should_be_disabled
```
element_should_be_disabled(locator, loglevel='INFO')
```
#### element_should_be_enabled
```
element_should_be_enabled(locator, loglevel='INFO')
```
#### element_should_be_visible
```
element_should_be_visible(locator, loglevel='INFO')
```
#### element_name_should_be
```
element_name_should_be(locator, expected)
```
#### element_value_should_be
```
element_value_should_be(locator, expected)
```
#### element_attribute_should_match
```
element_attribute_should_match(locator, attr_name, match_pattern, regexp=False)
```
#### element_should_contain_text
```
element_should_contain_text(locator, expected, message='')
```
#### element_should_not_contain_text
```
element_should_not_contain_text(locator, expected, message='')
```
#### element_text_should_be
```
element_text_should_be(locator, expected, message='')
```
#### get_webelement
```
get_webelement(locator)
```
#### get_webelements
```
get_webelements(locator)
```
#### get_element_attribute
```
get_element_attribute(locator, attribute)
```
#### get_element_location
```
get_element_location(locator)
```
#### get_element_size
```
get_element_size(locator)
```
#### get_text
```
get_text(locator)
```
#### get_matching_xpath_count
```
get_matching_xpath_count(xpath)
```
#### text_should_be_visible
```
text_should_be_visible(text, exact_match=False, loglevel='INFO')
```
#### xpath_should_match_x_times
```
xpath_should_match_x_times(xpath, count, error=None, loglevel='INFO')
```
## 部分内置函数(Core.Keywords.builtIn)
### XML文件操作
#### parse_xml
```
parse_xml(source, keep_clark_notation=False, strip_namespaces=False)
```
#### get_element
```
get_element(source, xpath='.')
```
#### get_elements
```
get_elements(source, xpath)
```
#### get_child_elements
```
get_child_elements(source, xpath='.')
```
#### get_element_count
```
get_element_count(source, xpath='.')
```
#### element_should_exist
```
element_should_exist(source, xpath='.', message=None)
```
#### element_should_not_exist
```
element_should_not_exist(source, xpath='.', message=None)
```
#### get_element_text
```
get_element_text(source, xpath='.', normalize_whitespace=False)
```
#### get_elements_texts
```
get_elements_texts(source, xpath, normalize_whitespace=False)
```
#### element_text_should_be
```
element_text_should_be(source, expected, xpath='.',
                               normalize_whitespace=False, message=None)
```
#### element_text_should_match
```
element_text_should_match(source, pattern, xpath='.',
                                  normalize_whitespace=False, message=None)
```
#### get_element_attribute
```
get_element_attribute(source, name, xpath='.', default=None)
```
#### get_element_attributes
```
get_element_attributes(source, xpath='.')
```
#### element_attribute_should_be
```
element_attribute_should_be(source, name, expected, xpath='.',
                                    message=None)
```
#### element_attribute_should_match
```
element_attribute_should_match(source, name, pattern, xpath='.',
                                       message=None)
```
#### element_should_not_have_attribute
```
element_should_not_have_attribute(source, name, xpath='.', message=None)
```
#### elements_should_be_equal
```
elements_should_be_equal(source, expected, exclude_children=False,
                                 normalize_whitespace=False)
```
#### elements_should_match
```
elements_should_match(source, expected, exclude_children=False,
                              normalize_whitespace=False)
```
#### set_element_tag
```
set_element_tag(source, tag, xpath='.')
```
#### set_elements_tag
```
set_elements_tag(source, tag, xpath='.')
```
#### set_element_text
```
set_element_text(source, text=None, tail=None, xpath='.')
```
#### set_elements_text
```
set_elements_text(source, text=None, tail=None, xpath='.')
```
#### set_element_attribute
```
set_element_attribute(source, name, value, xpath='.')
```
#### set_elements_attribute
```
set_elements_attribute(source, name, value, xpath='.')
```
#### remove_element_attribute
```
remove_element_attribute(source, name, xpath='.')
```
#### remove_elements_attribute
```
remove_elements_attribute(source, name, xpath='.')
```
#### remove_element_attributes
```
remove_element_attributes(source, xpath='.')
```
#### remove_elements_attributes
```
remove_elements_attributes(source, xpath='.')
```
#### add_element
```
add_element(source, element, index=None, xpath='.')
```
#### remove_element
```
remove_element(source, xpath='', remove_tail=False)
```
#### remove_elements
```
remove_elements(source, xpath='', remove_tail=False)
```
#### clear_element
```
clear_element(source, xpath='.', clear_tail=False)
```
#### copy_element
```
copy_element(source, xpath='.')
```
#### element_to_string
```
element_to_string(source, xpath='.', encoding=None)
```
#### log_element
```
log_element(source, level='INFO', xpath='.')
```
#### save_xml
```
save_xml(source, path, encoding='UTF-8')
```
#### evaluate_xpath
```
evaluate_xpath(source, expression, context='.')
```
### Telnet相关操作
#### open_connection
```
open_connection(host, alias=None, port=23, timeout=None,
                newline=None, prompt=None, prompt_is_regexp=False,
                encoding=None, encoding_errors=None,
                default_log_level=None, window_size=None,
                environ_user=None, terminal_emulation=None,
                terminal_type=None, telnetlib_log_level=None,
                connection_timeout=None)
```
#### switch_connection
```
switch_connection(index_or_alias)
```
#### close_all_connections
```
close_all_connections()
```
#### set_timeout
```
set_timeout(timeout)
```
#### set_newline
```
set_newline(newline)
```
#### set_prompt
```
set_prompt(prompt, prompt_is_regexp=False)
```
#### set_encoding
```
set_encoding(encoding=None, errors=None)
```
#### set_telnetlib_log_level
```
set_telnetlib_log_level(level)
```
#### set_default_log_level
```
set_default_log_level(level)
```
#### close_connection
```
close_connection(loglevel=None)
```
#### login
```
login(username, password, login_prompt='login: ',
      password_prompt='Password: ', login_timeout='1 second',
      login_incorrect='Login incorrect')
```
#### write
```
write(text, loglevel=None)
```
#### write_bare
```
write_bare(text)
```
#### write_until_expected_output
```
write_until_expected_output(text, expected, timeout,
                            retry_interval, loglevel=None)
```
#### write_control_character
```
write_control_character(character)
```
#### read
```
read(loglevel=None)
```
#### read_until
```
read_until(expected, loglevel=None)
```
#### read_until_regexp
```
read_until_regexp(*expected)
```
#### read_until_prompt
```
read_until_prompt(loglevel=None, strip_prompt=False)
```
#### execute_command
```
execute_command(command, loglevel=None, strip_prompt=False)
```
### Process相关
#### run_process
```
run_process(command, *arguments, **configuration)
```
#### start_process
```
start_process(command, *arguments, **configuration)
```
#### is_process_running
```
is_process_running(handle=None)
```
#### process_should_be_running
```
process_should_be_running(handle=None, error_message='Process is not running.')
```
#### process_should_be_stopped
```
process_should_be_stopped(handle=None, error_message='Process is running.')
```
#### wait_for_process
```
wait_for_process(handle=None, timeout=None, on_timeout='continue')
```
#### terminate_process
```
terminate_process(handle=None, kill=False)
```
#### terminate_all_processes
```
terminate_all_processes(kill=False)
```
#### send_signal_to_process
```
send_signal_to_process(signal, handle=None, group=False)
```
#### get_process_id
```
get_process_id(handle=None)
```
#### get_process_object
```
get_process_object(handle=None)
```
#### get_process_result
```
get_process_result(handle=None, rc=False, stdout=False,
                   stderr=False, stdout_path=False, stderr_path=False)
```
#### switch_process
```
switch_process(handle)
```
#### split_command_line
```
split_command_line(args, escaping=False)
```
#### join_command_line
```
join_command_line(*args)
```
