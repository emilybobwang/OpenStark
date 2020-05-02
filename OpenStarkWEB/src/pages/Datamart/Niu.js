import React from 'react';
import {
  Row,
  Col,
  Tabs,
  Steps,
  Collapse,
  Divider,
  Table,
  Button,
  Switch,
  Icon,
  Checkbox,
  Select,
  InputNumber,
  Input,
  Radio,
  Popconfirm,
} from 'antd';
import { connect } from 'dva';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';

const { TabPane } = Tabs;
const { Step } = Steps;
const { Panel } = Collapse;
const { Option } = Select;
const { Group: CheckboxGroup } = Checkbox;
const { Group: RadioGroup } = Radio;

const tcColumns = [
  {
    title: '序号',
    dataIndex: 'key',
    key: 'key',
  },
  {
    title: '接口名称',
    dataIndex: 'label',
    key: 'label',
  },
  {
    title: '接口地址',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: '执行结果',
    dataIndex: 'result',
    key: 'result',
    render: (text, record) => (
      <Popconfirm
        title={
          <Input.TextArea
            value={JSON.stringify(JSON.parse(record.resp), null, 2)}
            style={{ width: 800, height: 600 }}
          />
        }
      >
        {text}
      </Popconfirm>
    ),
  },
  {
    title: '运行状态',
    dataIndex: 'status',
    key: 'status',
  },
];

@connect(({ niu, loading }) => ({
  niu,
  loading,
}))
class NiuPage extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      // weblog
      sendMsg: '',
      result: '',
      ws: null,
      clientId: 0,
      // 分类日志
      tasks: null,
      userCount: 3,
      mobileCount: 2,
      postRaParams: {
        type: ['register', 'real', 'banding', 'recharge'],
        mobile: '',
        password: 't1234567',
        password_enc: '',
        jy_password: '123456',
        planner: '',
        market: '0',
        amount: '5000.00',
        count: '1',
        op: 'user_data',
        host: '',
        act: 'register-all',
      },
      postLoanParams: {
        op: 'product_data',
        host: '172.20.20.11',
        act: 'loan',
        client_id: '',
        type: '0',
        count: '1',
        amount: '5000.00',
        term: '12',
        term_mode: '1',
        annual_rate: '15.00',
        repayment: '0',
        publish: '2',
        loan_type: '1',
      },
      postSingleParams: {
        op: 'product_data',
        host: '172.20.20.11',
        act: 'single',
        type: '0',
        client_id: '',
        count: '1',
        amount: '5000.00',
        term: '12',
        term_mode: '2',
        annual_rate: '15.00',
        repayment: '0',
        transfer: '0',
        loan_type: '1',
      },
      raType: {
        register: '注册',
        real: '实名',
        banding: '绑卡',
        recharge: '充值',
        mc_recharge: '挡板绑卡',
        cg_banding: '存管绑卡',
        mc_banding: '挡板充值',
        cg_recharge: '存管充值',
      },
      // 输入窗口
      inputWindowDisplay: 'flex',
      // 输出窗口
      outputWindowDisplay: 'flex',
      outputActiveKey: '1',
      // 当前的环境
      currentEnv: '请选择测试环境',
      // 按钮默认状态
      btnFlag: true,
    };

    this.onRefreshUserDataChange = this.onRefreshUserDataChange.bind(this);
    this.onInputTabChange = this.onInputTabChange.bind(this);
    this.onSelectEnvChange = this.onSelectEnvChange.bind(this);
    this.onUserTypeChange = this.onUserTypeChange.bind(this);
    this.onRaBtnChange = this.onRaBtnChange.bind(this);
    this.onLoanBtnChange = this.onLoanBtnChange.bind(this);
    this.onSingleBtnChange = this.onSingleBtnChange.bind(this);
    this.onRaParamChange = this.onRaParamChange.bind(this);
    this.onLoanParamChange = this.onLoanParamChange.bind(this);
    this.onSingleParamChange = this.onSingleParamChange.bind(this);
    this.onSwitchOn = this.onSwitchOn.bind(this);
    this.onTaskChange = this.onTaskChange.bind(this);

    this.renderTestSuite = this.renderTestSuite.bind(this);
  }

  componentDidMount() {
    const { dispatch } = this.props;
    const { userCount, mobileCount } = this.state;
    this.connect();

    dispatch({
      type: 'niu/getUserData', // 需要传递的信息
      payload: {
        count: userCount,
      },
    });
    dispatch({
      type: 'niu/getHostsData', // 需要传递的信息
      payload: {
        count: 3,
      },
    });
    dispatch({
      type: 'niu/getMobilesData', // 需要传递的信息
      payload: {
        count: mobileCount,
      },
    });
    dispatch({
      type: 'niu/getTasksData', // 需要传递的信息
      payload: {
        count: mobileCount,
      },
    });

    this.initPageData();
  }

  onclose = () => {
    this.setState({
      ws: null,
    });
  };

  onopen = () => {
    // const { ws } = this.state;
    // ws.send(JSON.stringify({ "op":"echo", "message":"你好，我是AceDou!" }));
  };

  onmessage = ({ data }) => {
    this.setState({ result: data });
    try {
      const cmd = JSON.parse(data);
      this.doMessage(cmd);
    } catch (e) {
      console.log(e);
    }
  };

  clearOnClick = () => {
    this.setState({
      sendMsg: '',
    });
  };

  sendOnClick = type => () => {
    const { ws, sendMsg } = this.state;

    if (ws === null) {
      if (type === 100) {
        this.connect();
        return;
      }

      this.setState({
        result: '连接已经断开',
      });
      return;
    }

    if (type === 0) {
      ws.send(JSON.stringify(sendMsg));
    } else if (type === 1) {
      ws.send(
        JSON.stringify({
          op: 'tasks',
        })
      );
    } else if (type === 2) {
      ws.send(
        JSON.stringify({
          op: 'client_id',
        })
      );
    } else if (type === 3) {
      ws.send(
        JSON.stringify({
          op: 'jobs',
        })
      );
    } else if (type === 100) {
      if (ws != null) {
        ws.close();
      }
      this.connect();
    } else if (type === 101) {
      if (ws != null) {
        ws.close();
        this.setState({
          ws: null,
        });
      }
    } else if (type === 999) {
      ws.send(
        JSON.stringify({
          op: 'heart_beat',
          value: new Date().getTime(),
        })
      );
    }
  };

  doMessage(cmd) {
    console.log(cmd);
    switch (cmd.op) {
      case 'client_id': {
        this.setState({
          clientId: parseInt(cmd.response.client_id),
          result: cmd.response.client_id,
        });
      }
      case 'tasks': {
        this.setState({
          tasks: cmd.response.tasks,
        });
      }
      // case ('jobs_update'): {
      //   this.setState(
      //     {
      //       tasks:cmd.response.tasks,
      //     }
      //   )
      // }
      default: {
        console.log(cmd);
      }
    }
  }

  connect() {
    const ws = new WebSocket('ws://172.20.20.160:8099/api/weblogs');

    ws.onmessage = this.onmessage;
    ws.onclose = this.onclose;
    ws.onopen = this.onopen;
    this.setState({
      ws,
    });
  }

  onTaskChange = activeKey => {
    this.setState({
      outputActiveKey: activeKey,
    });
  };

  onRefreshUserDataChange = count => () => {
    const { dispatch } = this.props;

    this.setState({
      userCount: count,
    });

    dispatch({
      type: 'niu/getUserData',
      payload: {
        count,
      },
    });
  };

  onSwitchOn = (op, act, host) => checked => {
    console.log(op, act, host, checked);
    if (checked) {
      const { dispatch } = this.props;
      dispatch({
        type: 'niu/postSwitch',
        payload: {
          op,
          act,
          host,
        },
      });
    }
  };

  onInputTabChange(activeKey) {
    this.setState({
      outputActiveKey: activeKey,
    });

    if (activeKey === 'ra' || activeKey === 'loan' || activeKey === 'single') {
      this.showWindow(true, true);
    } else {
      this.showWindow(true, false);
    }
  }

  onRaBtnChange = btType => () => {
    const { postRaParams, clientId, currentEnv } = this.state;
    const { dispatch } = this.props;

    postRaParams.client_id = clientId;
    postRaParams.host = currentEnv;

    if (btType === 1) {
      postRaParams.type = ['regiester', 'real', 'banding', 'recharge'];
    } else if (btType === 2) {
      postRaParams.type = ['regiester', 'real', 'cg_banding', 'cg_recharge'];
    }

    this.setState({
      postRaParams: {
        ...postRaParams,
      },
      outputActiveKey: 'ra',
    });
  
    if (postRaParams.password !== "t1234567" && postRaParams.password !== ""){
      dispatch({
        type: 'niu/getEncryptPassword',
        payload: {
          password: postRaParams.password,
        },
      }).then(
        () => {
          const { niu } = this.props;
          postRaParams.password_enc = niu.password_enc;
          dispatch({
            type: 'niu/postRa',
            payload: {
              ...postRaParams,
            },
          });
        }
      );
    } else {
      dispatch({
        type: 'niu/postRa',
        payload: {
          ...postRaParams,
        },
      });
    }
  };

  onSingleBtnChange = btType => () => {
    const { postSingleParams, clientId, currentEnv } = this.state;
    const { dispatch } = this.props;

    postSingleParams.client_id = clientId;
    postSingleParams.host = currentEnv;

    if (btType === 1) {
      postSingleParams.type = '0';
      postSingleParams.loan_type = '1';
    } else if (btType === 2) {
      postSingleParams.type = '0';
      postSingleParams.loan_type = '0';
    }

    this.setState({
      postSingleParams: {
        ...postSingleParams,
      },
      outputActiveKey: 'single',
    });

    dispatch({
      type: 'niu/postSingle',
      payload: {
        ...postSingleParams,
      },
    });
  };

  onLoanBtnChange = btType => () => {
    const { postLoanParams, clientId, currentEnv } = this.state;
    const { dispatch } = this.props;

    postLoanParams.client_id = clientId;
    postLoanParams.host = currentEnv;

    if (btType === 1) {
      postLoanParams.type = '0';
      postLoanParams.loan_type = '1';
    } else if (btType === 2) {
      postLoanParams.type = '0';
      postLoanParams.loan_type = '0';
    }

    this.setState({
      postLoanParams: {
        ...postLoanParams,
      },
      outputActiveKey: 'loan',
    });

    dispatch({
      type: 'niu/postLoan',
      payload: {
        ...postLoanParams,
      },
    });
  };

  onSelectEnvChange(value) {
    this.setState({
      currentEnv: value,
      btnFlag: false,
    });
  }

  onRaParamChange = paraName => eOrValue => {
    const { postRaParams } = this.state;
    console.log('onRaParamChange/type:', paraName);
    if (eOrValue instanceof Object) {
      postRaParams[paraName] = eOrValue.target.value;
    } else {
      postRaParams[paraName] = eOrValue;
    }

    this.setState({
      postRaParams: {
        ...postRaParams,
      },
    });
  };

  onLoanParamChange = paraName => eOrValue => {
    const { postLoanParams } = this.state;

    if (eOrValue instanceof Object) {
      postLoanParams[paraName] = eOrValue.target.value;
    } else {
      postLoanParams[paraName] = eOrValue;
    }

    this.setState({
      postLoanParams: {
        ...postLoanParams,
      },
    });
  };

  onSingleParamChange = paraName => eOrValue => {
    const { postSingleParams } = this.state;

    if (eOrValue instanceof Object) {
      postSingleParams[paraName] = eOrValue.target.value;
    } else {
      postSingleParams[paraName] = eOrValue;
    }

    this.setState({
      postLoanParams: {
        ...postSingleParams,
      },
    });
  };

  showWindow = (flagShowInputWidow = true, flagShowOutputWidow = false) => {
    this.setState({
      inputWindowDisplay: flagShowInputWidow ? 'block' : 'none',
      outputWindowDisplay: flagShowOutputWidow ? 'block' : 'none',
    });
  };

  onUserTypeChange = e => {
    const { postRaParams } = this.state;
    postRaParams.type = e;
    console.log(postRaParams);
    this.setState({
      postRaParams: {
        ...postRaParams,
      },
    });
  };

  initPageData() {
    const { niu } = this.props;
    const { Mobiles } = niu;
    const { postRaParams } = this.state;

    this.setState(
      {
        postRaParams: {
          ...postRaParams,
          mobile: Mobiles[0] !== undefined ? Mobiles[0] : '',
          planner: Mobiles[1] !== undefined ? Mobiles[1] : '',
        },
      },
      this.initPageShow
    );
  }

  initPageShow() {
    this.showWindow(true, true);
  }

  renderSingle() {
    const renderItem = [];
    const { niu } = this.props;
    const { SingleMessage } = niu;
    const { currentEnv, postSingleParams, btnFlag, tasks } = this.state;
    const {
      type,
      term,
      term_mode: termMode,
      count,
      amount,
      annual_rate: annualRate,
      repayment,
      transfer,
      loan_type: loanType,
    } = postSingleParams;

    renderItem.push(<Divider key="DividerSingle0">测试环境</Divider>);

    renderItem.push(
      <Row gutter={24} key="SingleRowEnv0">
        <Col span={8} style={{ textAlign: 'right' }}>
          按代号
        </Col>
        <Col span={4} style={{ textAlign: 'left' }}>
          <Select
            labelInValue={false}
            value={currentEnv}
            placeholder="请选择测试环境"
            style={{ width: 170 }}
            size="small"
            onChange={this.onSelectEnvChange}
          >
            {this.renderEnvOption(false)}
          </Select>
        </Col>
        <Col span={2} style={{ textAlign: 'right' }}>
          按IP
        </Col>
        <Col span={10} style={{ textAlign: 'left' }}>
          <Select
            labelInValue={false}
            value={currentEnv}
            placeholder="请选择测试环境"
            style={{ width: 170 }}
            size="small"
            onChange={this.onSelectEnvChange}
          >
            {this.renderEnvOption(true)}
          </Select>
        </Col>
      </Row>
    );
    renderItem.push(<Divider key="DividerSingle1">业务选项</Divider>);
    renderItem.push(
      <Row gutter={24} key="SingleRow0">
        <Col span={8} style={{ textAlign: 'right' }}>
          资产类型
        </Col>
        <Col span={4} style={{ textAlign: 'left' }}>
          <RadioGroup value={type} onChange={this.onSingleParamChange('type')}>
            <Radio value="0">个人</Radio>
            <Radio value="1">企业</Radio>
          </RadioGroup>
        </Col>
        <Col span={2} style={{ textAlign: 'right' }}>
          是否存管
        </Col>
        <Col span={10} style={{ textAlign: 'left' }}>
          <RadioGroup value={loanType} onChange={this.onSingleParamChange('loan_type')}>
            <Radio value="0">存管标</Radio>
            <Radio value="1">非存管标</Radio>
          </RadioGroup>
        </Col>
      </Row>
    );

    renderItem.push(
      <Row gutter={24} key="SingleRow1">
        <Col span={8} style={{ textAlign: 'right' }}>
          个数
        </Col>
        <Col span={4} style={{ textAlign: 'left' }}>
          <InputNumber
            min={1}
            max={100}
            value={count}
            size="small"
            style={{ width: 170 }}
            onChange={this.onSingleParamChange('count')}
          />
        </Col>
        <Col span={2} style={{ textAlign: 'right' }}>
          金额(元)
        </Col>
        <Col span={10} style={{ textAlign: 'left' }}>
          <InputNumber
            min={1}
            max={20000}
            value={amount}
            size="small"
            style={{ width: 170 }}
            onChange={this.onSingleParamChange('amount')}
          />
        </Col>
      </Row>
    );

    const selectAfter = (
      <Select
        value={termMode}
        style={{ width: 80 }}
        onChange={this.onSingleParamChange('term_mode')}
      >
        <Option value="1">天</Option>
        <Option value="2">月</Option>
        <Option value="3">年</Option>
      </Select>
    );

    renderItem.push(
      <Row gutter={24} key="SingleRow2">
        <Col span={8} style={{ textAlign: 'right' }}>
          期限
        </Col>
        <Col span={4} style={{ textAlign: 'left' }}>
          <Input
            size="small"
            placeholder="期限"
            addonAfter={selectAfter}
            style={{ width: 170 }}
            value={term}
            onChange={this.onSingleParamChange('term')}
          />
        </Col>
        <Col span={2} style={{ textAlign: 'right' }}>
          利率(%)
        </Col>
        <Col span={10} style={{ textAlign: 'left' }}>
          <Input
            size="small"
            placeholder="利率(%)"
            style={{ width: 170 }}
            value={annualRate}
            onChange={this.onSingleParamChange('annual_rate')}
          />
        </Col>
      </Row>
    );

    renderItem.push(
      <Row gutter={24} key="SingleRow3">
        <Col span={8} style={{ textAlign: 'right' }}>
          还款方式
        </Col>
        <Col span={4} style={{ textAlign: 'left' }}>
          <Select
            value={repayment}
            style={{ width: 170 }}
            size="small"
            onChange={this.onSingleParamChange('repayment')}
          >
            <Option value="0">一次性还款</Option>
            <Option value="1">等额本息</Option>
            <Option value="3">先息后本</Option>
            <Option value="5">每月还本付息</Option>
            <Option value="1">按期还本息</Option>
          </Select>
        </Col>
        <Col span={2} style={{ textAlign: 'right' }}>
          是否可转
        </Col>
        <Col span={10} style={{ textAlign: 'left' }}>
          <RadioGroup value={transfer} onChange={this.onSingleParamChange('transfer')}>
            <Radio value="0">是</Radio>
            <Radio value="1">否</Radio>
          </RadioGroup>
        </Col>
      </Row>
    );

    renderItem.push(<Divider key="DividerSingle2">^-^</Divider>);
    renderItem.push(
      <Row gutter={24} key="SingleRow4">
        <Col span={8} style={{ textAlign: 'right' }}>
          &nbsp;
        </Col>
        <Col span={4} style={{ textAlign: 'left' }}>
          <Button
            type="primary"
            htmlType="button"
            onClick={this.onSingleBtnChange(1)}
            disabled={btnFlag}
          >
            提交任务
          </Button>
        </Col>
        <Col span={12} style={{ textAlign: 'left' }}>
          <Button
            type="dashed"
            htmlType="button"
            onClick={this.onSingleBtnChange(2)}
            disabled={btnFlag}
          >
            热门任务(个人+存管)
          </Button>
          <Button
            type="dashed"
            htmlType="button"
            onClick={this.onSingleBtnChange(3)}
            disabled={btnFlag}
          >
            热门任务(个人+非存管)
          </Button>
        </Col>
      </Row>
    );

    if (tasks != null) {
      if (Object.keys(tasks).indexOf('single') > -1) {
        const task = tasks.single;
        const { result } = task;
        renderItem.push(<Divider key="DividerSingle3">成功数据</Divider>);
        renderItem.push(
          <Row gutter={24} key="top0">
            <Col span={1} style={{ textAlign: 'center' }}>
              序号
            </Col>
            <Col span={1} style={{ textAlign: 'center' }}>
              姓名
            </Col>
            <Col span={2} style={{ textAlign: 'center' }}>
              姓名读音
            </Col>
            <Col span={2} style={{ textAlign: 'center' }}>
              手机号码
            </Col>
            <Col span={2} style={{ textAlign: 'center' }}>
              合同编号
            </Col>
            <Col span={2} style={{ textAlign: 'center' }}>
              银行卡号
            </Col>
            <Col span={4} style={{ textAlign: 'center' }}>
              银行分行
            </Col>
            <Col span={2} style={{ textAlign: 'center' }}>
              银行编码
            </Col>
            <Col span={2} style={{ textAlign: 'center' }}>
              身份证号码
            </Col>
            <Col span={1} style={{ textAlign: 'center' }}>
              金额
            </Col>
            <Col span={2} style={{ textAlign: 'center' }}>
              登记时间
            </Col>
            <Col span={1} style={{ textAlign: 'center' }}>
              年利率(%)
            </Col>
          </Row>
        );
        for (let index = 0; index < result.length; index += 1) {
          const resultItem = result[index];
          renderItem.push(
            <Row gutter={24} key={index}>
              <Col span={1} style={{ textAlign: 'center' }}>
                {index + 1}
              </Col>
              <Col span={1} style={{ textAlign: 'center' }}>
                {resultItem['姓名']}
              </Col>
              <Col span={2} style={{ textAlign: 'center' }}>
                {resultItem['姓名读音']}
              </Col>
              <Col span={2} style={{ textAlign: 'center' }}>
                {resultItem['手机号码']}
              </Col>
              <Col span={2} style={{ textAlign: 'center' }}>
                {resultItem['合同编号']}
              </Col>
              <Col span={2} style={{ textAlign: 'center' }}>
                {resultItem['银行卡号']}
              </Col>
              <Col span={4} style={{ textAlign: 'center' }}>
                {resultItem['银行分行']}
              </Col>
              <Col span={2} style={{ textAlign: 'center' }}>
                {resultItem['银行编码']}
              </Col>
              <Col span={2} style={{ textAlign: 'center' }}>
                {resultItem['身份证号码']}
              </Col>
              <Col span={1} style={{ textAlign: 'center' }}>
                {resultItem['金额']}
              </Col>
              <Col span={2} style={{ textAlign: 'center' }}>
                {resultItem['登记时间']}
              </Col>
              <Col span={1} style={{ textAlign: 'center' }}>
                {resultItem['年利率']}
              </Col>
            </Row>
          );
        }
      }
    }

    if (SingleMessage !== '') {
      renderItem.push(<Divider key="DividerSingle4">执行结果</Divider>);
      renderItem.push(
        <Row gutter={24} key="RegisterAllRow6">
          <Col span={24} style={{ textAlign: 'center' }}>
            {SingleMessage}
          </Col>
        </Row>
      );
    }

    return renderItem;
  }

  renderLoan() {
    const renderItem = [];
    const { niu } = this.props;
    const { LoanMessage } = niu;
    const { currentEnv, postLoanParams, btnFlag, tasks } = this.state;
    const {
      type,
      term,
      term_mode: termMode,
      count,
      amount,
      annual_rate: annualRate,
      repayment,
      publish,
      loan_type: loanType,
    } = postLoanParams;

    renderItem.push(<Divider key="DividerLoanRow0">测试环境</Divider>);

    renderItem.push(
      <Row gutter={24} key="LoanRowEnv0">
        <Col span={8} style={{ textAlign: 'right' }}>
          按代号
        </Col>
        <Col span={4} style={{ textAlign: 'left' }}>
          <Select
            labelInValue={false}
            value={currentEnv}
            placeholder="请选择测试环境"
            style={{ width: 170 }}
            size="small"
            onChange={this.onSelectEnvChange}
          >
            {this.renderEnvOption(false)}
          </Select>
        </Col>
        <Col span={2} style={{ textAlign: 'right' }}>
          按IP
        </Col>
        <Col span={10} style={{ textAlign: 'left' }}>
          <Select
            labelInValue={false}
            value={currentEnv}
            placeholder="请选择测试环境"
            style={{ width: 170 }}
            size="small"
            onChange={this.onSelectEnvChange}
          >
            {this.renderEnvOption(true)}
          </Select>
        </Col>
      </Row>
    );
    renderItem.push(<Divider key="DividerLoanRow1">业务选项</Divider>);
    renderItem.push(
      <Row gutter={24} key="LoanRow0">
        <Col span={8} style={{ textAlign: 'right' }}>
          类型
        </Col>
        <Col span={4} style={{ textAlign: 'left' }}>
          <RadioGroup value={type} onChange={this.onLoanParamChange('type')}>
            <Radio value="0">个人</Radio>
            <Radio value="1">企业</Radio>
          </RadioGroup>
        </Col>
        <Col span={2} style={{ textAlign: 'right' }}>
          是否存管
        </Col>
        <Col span={10} style={{ textAlign: 'left' }}>
          <RadioGroup value={loanType} onChange={this.onLoanParamChange('loan_type')}>
            <Radio value="0">存管标</Radio>
            <Radio value="1">非存管标</Radio>
          </RadioGroup>
        </Col>
      </Row>
    );

    renderItem.push(
      <Row gutter={24} key="LoanRow1">
        <Col span={8} style={{ textAlign: 'right' }}>
          个数
        </Col>
        <Col span={4} style={{ textAlign: 'left' }}>
          <InputNumber
            min={1}
            max={100}
            value={count}
            size="small"
            style={{ width: 170 }}
            onChange={this.onLoanParamChange('count')}
          />
        </Col>
        <Col span={2} style={{ textAlign: 'right' }}>
          金额(元)
        </Col>
        <Col span={10} style={{ textAlign: 'left' }}>
          <InputNumber
            min={100}
            max={200000}
            value={amount}
            size="small"
            style={{ width: 170 }}
            onChange={this.onLoanParamChange('amount')}
          />
        </Col>
      </Row>
    );

    const selectAfter = (
      <Select
        defaultValue="1"
        value={termMode}
        style={{ width: 80 }}
        onChange={this.onLoanParamChange('term_mode')}
      >
        <Option value="0">天</Option>
        <Option value="1" selected>
          月
        </Option>
        <Option value="2">年</Option>
      </Select>
    );

    renderItem.push(
      <Row gutter={24} key="LoanRow2">
        <Col span={8} style={{ textAlign: 'right' }}>
          期限
        </Col>
        <Col span={4} style={{ textAlign: 'left' }}>
          <Input
            size="small"
            placeholder="期限"
            addonAfter={selectAfter}
            style={{ width: 170 }}
            value={term}
            onChange={this.onLoanParamChange('term')}
          />
        </Col>
        <Col span={2} style={{ textAlign: 'right' }}>
          利率(%)
        </Col>
        <Col span={10} style={{ textAlign: 'left' }}>
          <Input
            size="small"
            placeholder="利率(%)"
            style={{ width: 170 }}
            value={annualRate}
            onChange={this.onLoanParamChange('annual_rate')}
          />
        </Col>
      </Row>
    );

    renderItem.push(
      <Row gutter={24} key="LoanRow3">
        <Col span={8} style={{ textAlign: 'right' }}>
          还款方式
        </Col>
        <Col span={4} style={{ textAlign: 'left' }}>
          <Select
            defaultValue="0"
            style={{ width: 170 }}
            size="small"
            value={repayment}
            onChange={this.onLoanParamChange('repayment')}
          >
            <Option value="0">一次性还款</Option>
            <Option value="1">等额本息</Option>
            <Option value="3">先息后本</Option>
            <Option value="5">每月还本付息</Option>
            <Option value="1">按期还本息</Option>
          </Select>
        </Col>
        <Col span={2} style={{ textAlign: 'right' }}>
          是否推送
        </Col>
        <Col span={10} style={{ textAlign: 'left' }}>
          <RadioGroup value={publish} onChange={this.onLoanParamChange('publish')}>
            <Radio value="1">是</Radio>
            <Radio value="2">否</Radio>
          </RadioGroup>
        </Col>
      </Row>
    );

    renderItem.push(<Divider key="DividerLoanRow2">^-^</Divider>);
    renderItem.push(
      <Row gutter={24} key="LoanRow4">
        <Col span={8} style={{ textAlign: 'right' }}>
          &nbsp;
        </Col>
        <Col span={4} style={{ textAlign: 'left' }}>
          <Button
            type="primary"
            htmlType="button"
            onClick={this.onLoanBtnChange(0)}
            disabled={btnFlag}
          >
            提交任务
          </Button>
        </Col>
        <Col span={12} style={{ textAlign: 'left' }}>
          <Button
            type="dashed"
            htmlType="button"
            onClick={this.onLoanBtnChange(1)}
            disabled={btnFlag}
          >
            热门任务(个人+存管)
          </Button>
          <Button
            type="dashed"
            htmlType="button"
            onClick={this.onLoanBtnChange(2)}
            disabled={btnFlag}
          >
            热门任务(个人+非存管)
          </Button>
        </Col>
      </Row>
    );

    if (tasks != null) {
      if (Object.keys(tasks).indexOf('loan') > -1) {
        const task = tasks.loan;
        const { result } = task;
        renderItem.push(<Divider key="DividerLoan3">成功数据</Divider>);
        renderItem.push(
          <Row gutter={24} key="top0">
            <Col span={1} style={{ textAlign: 'center' }}>
              序号
            </Col>
            <Col span={1} style={{ textAlign: 'center' }}>
              姓名
            </Col>
            <Col span={2} style={{ textAlign: 'center' }}>
              姓名读音
            </Col>
            <Col span={2} style={{ textAlign: 'center' }}>
              手机号码
            </Col>
            <Col span={2} style={{ textAlign: 'center' }}>
              合同编号
            </Col>
            <Col span={2} style={{ textAlign: 'center' }}>
              银行卡号
            </Col>
            <Col span={4} style={{ textAlign: 'center' }}>
              银行分行
            </Col>
            <Col span={2} style={{ textAlign: 'center' }}>
              银行编码
            </Col>
            <Col span={2} style={{ textAlign: 'center' }}>
              身份证号码
            </Col>
            <Col span={1} style={{ textAlign: 'center' }}>
              金额
            </Col>
            <Col span={2} style={{ textAlign: 'center' }}>
              登记时间
            </Col>
            <Col span={1} style={{ textAlign: 'center' }}>
              年利率(%)
            </Col>
          </Row>
        );
        for (let index = 0; index < result.length; index += 1) {
          const resultItem = result[index];
          renderItem.push(
            <Row gutter={24} key={index}>
              <Col span={1} style={{ textAlign: 'center' }}>
                {index + 1}
              </Col>
              <Col span={1} style={{ textAlign: 'center' }}>
                {resultItem['姓名']}
              </Col>
              <Col span={2} style={{ textAlign: 'center' }}>
                {resultItem['姓名读音']}
              </Col>
              <Col span={2} style={{ textAlign: 'center' }}>
                {resultItem['手机号码']}
              </Col>
              <Col span={2} style={{ textAlign: 'center' }}>
                {resultItem['合同编号']}
              </Col>
              <Col span={2} style={{ textAlign: 'center' }}>
                {resultItem['银行卡号']}
              </Col>
              <Col span={4} style={{ textAlign: 'center' }}>
                {resultItem['银行分行']}
              </Col>
              <Col span={2} style={{ textAlign: 'center' }}>
                {resultItem['银行编码']}
              </Col>
              <Col span={2} style={{ textAlign: 'center' }}>
                {resultItem['身份证号码']}
              </Col>
              <Col span={1} style={{ textAlign: 'center' }}>
                {resultItem['金额']}
              </Col>
              <Col span={2} style={{ textAlign: 'center' }}>
                {resultItem['登记时间']}
              </Col>
              <Col span={1} style={{ textAlign: 'center' }}>
                {resultItem['年利率']}
              </Col>
            </Row>
          );
        }
      }
    }

    if (LoanMessage !== '') {
      renderItem.push(<Divider key="DividerLoanRow3">执行结果</Divider>);
      renderItem.push(
        <Row gutter={24} key="RegisterAllRow6">
          <Col span={24} style={{ textAlign: 'center' }}>
            {LoanMessage}
          </Col>
        </Row>
      );
    }
    return renderItem;
  }

  renderEnvOption(flagShowIp) {
    const optionList = [];
    const { niu } = this.props;
    const { Hosts } = niu;
    for (let index = 0; index < Hosts.length; index += 1) {
      const host = Hosts[index];
      if (flagShowIp) {
        optionList.push(
          <Option value={host.ip} key={`Option${index}`}>
            {host.ip}
          </Option>
        );
      } else {
        const ipEnd = host.ip.split('.')[3];
        const envName = `${ipEnd.substr(-3, ipEnd.length - 1)}X段环境`;
        optionList.push(
          <Option value={host.ip} key={`Option${index}`}>
            {envName}
          </Option>
        );
      }
    }
    return optionList;
  }

  renderRaType() {
    const renderItem = [];
    const { raType } = this.state;
    Object.keys(raType).forEach(key => {
      const label = raType[key];
      renderItem.push(
        <Checkbox value={key} key={key}>
          {label}
        </Checkbox>
      );
    });
    return renderItem;
  }

  renderRegisterAll() {
    const renderItem = [];
    const { niu } = this.props;
    const { Mobiles: mobiles, RaMessage } = niu;
    const { currentEnv, postRaParams, btnFlag, tasks } = this.state;
    const {
      type,
      mobile,
      password,
      jy_password: jyPassword,
      planner,
      market,
      amount,
      count,
    } = postRaParams;

    renderItem.push(<Divider key="DividerRegisterAll0">测试环境</Divider>);

    renderItem.push(
      <Row gutter={24} key="LoanRowEnv0">
        <Col span={8} style={{ textAlign: 'right' }}>
          按代号
        </Col>
        <Col span={4} style={{ textAlign: 'left' }}>
          <Select
            labelInValue={false}
            placeholder="请选择测试环境"
            value={currentEnv}
            style={{ width: 170 }}
            size="small"
            onChange={this.onSelectEnvChange}
          >
            {this.renderEnvOption(false)}
          </Select>
        </Col>
        <Col span={2} style={{ textAlign: 'right' }}>
          按IP
        </Col>
        <Col span={10} style={{ textAlign: 'left' }}>
          <Select
            labelInValue={false}
            placeholder="请选择测试环境"
            value={currentEnv}
            style={{ width: 170 }}
            size="small"
            onChange={this.onSelectEnvChange}
          >
            {this.renderEnvOption(true)}
          </Select>
        </Col>
      </Row>
    );
    renderItem.push(<Divider key="DividerRegisterAll1">业务选项</Divider>);

    renderItem.push(
      <Row gutter={24} key="RegisterAllRow0">
        <Col span={8} style={{ textAlign: 'right' }}>
          类型
        </Col>
        <Col span={6} style={{ textAlign: 'left' }}>
          <CheckboxGroup onChange={this.onUserTypeChange} defaultValue={type}>
            {this.renderRaType()}
          </CheckboxGroup>
        </Col>
        <Col span={10} style={{ textAlign: 'right' }}>
          &nbsp;
        </Col>
      </Row>
    );

    renderItem.push(
      <Row gutter={24} key="RegisterAllRow1">
        <Col span={8} style={{ textAlign: 'right' }}>
          个数
        </Col>
        <Col span={4} style={{ textAlign: 'left' }}>
          <InputNumber
            min={1}
            max={100}
            defaultValue={count}
            size="small"
            style={{ width: 170 }}
            onChange={this.onRaParamChange('count')}
          />
        </Col>
        <Col span={2} style={{ textAlign: 'right' }}>
          手机/用户名
        </Col>
        <Col span={10} style={{ textAlign: 'left' }}>
          <Input
            size="small"
            placeholder="手机号/用户名"
            style={{ width: 170 }}
            value={mobile}
            onChange={this.onRaParamChange('mobile')}
          />
        </Col>
      </Row>
    );

    renderItem.push(
      <Row gutter={24} key="RegisterAllRow2">
        <Col span={8} style={{ textAlign: 'right' }}>
          密码
        </Col>
        <Col span={4} style={{ textAlign: 'left' }}>
          <Input
            size="small"
            placeholder="small size"
            defaultValue="t123456"
            style={{ width: 170 }}
            value={password}
            onChange={this.onRaParamChange('password')}
          />
        </Col>
        <Col span={2} style={{ textAlign: 'right' }}>
          交易密码
        </Col>
        <Col span={10} style={{ textAlign: 'left' }}>
          <Input
            size="small"
            placeholder="small size"
            defaultValue="123456"
            style={{ width: 170 }}
            value={jyPassword}
            onChange={this.onRaParamChange('jy_password')}
          />
        </Col>
      </Row>
    );

    renderItem.push(
      <Row gutter={24} key="RegisterAllRow3">
        <Col span={8} style={{ textAlign: 'right' }}>
          推荐人手机/用户名
        </Col>
        <Col span={4} style={{ textAlign: 'left' }}>
          <Input
            size="small"
            placeholder="small size"
            defaultValue={mobiles[1]}
            style={{ width: 170 }}
            onChange={this.onRaParamChange('planner')}
            value={planner}
          />
        </Col>
        <Col span={2} style={{ textAlign: 'right' }}>
          渠道索引
        </Col>
        <Col span={10} style={{ textAlign: 'left' }}>
          <Input
            size="small"
            placeholder="small size"
            defaultValue="0"
            style={{ width: 170 }}
            onChange={this.onRaParamChange('market')}
            value={market}
          />
        </Col>
      </Row>
    );

    renderItem.push(
      <Row gutter={24} key="RegisterAllRow4">
        <Col span={8} style={{ textAlign: 'right' }}>
          充值金额(元)
        </Col>
        <Col span={4} style={{ textAlign: 'left' }}>
          <Input
            size="small"
            placeholder="small size"
            defaultValue="5000.00"
            style={{ width: 170 }}
            onChange={this.onRaParamChange('amount')}
            value={amount}
          />
        </Col>
        <Col span={2} style={{ textAlign: 'right' }}>
          &nbsp;
        </Col>
        <Col span={10} style={{ textAlign: 'left' }}>
          &nbsp;
        </Col>
      </Row>
    );

    renderItem.push(<Divider key="DividerRegisterAll2">^-^</Divider>);
    renderItem.push(
      <Row gutter={24} key="RegisterAllRow5">
        <Col span={8} style={{ textAlign: 'right' }}>
          &nbsp;
        </Col>
        <Col span={4} style={{ textAlign: 'left' }}>
          <Button
            htmlType="button"
            type="primary"
            onClick={this.onRaBtnChange(0)}
            disabled={btnFlag}
          >
            提交任务
          </Button>
        </Col>
        <Col span={12} style={{ textAlign: 'left' }}>
          <Button
            htmlType="button"
            type="dashed"
            onClick={this.onRaBtnChange(1)}
            disabled={btnFlag}
          >
            热门任务(非存管)
          </Button>
          <Button
            htmlType="button"
            type="dashed"
            onClick={this.onRaBtnChange(2)}
            disabled={btnFlag}
          >
            热门任务(存管)
          </Button>
        </Col>
      </Row>
    );

    if (tasks != null) {
      if (Object.keys(tasks).indexOf('ra') > -1) {
        const task = tasks.ra;
        const { result } = task;
        renderItem.push(<Divider key="DividerRegisterAll3">成功数据</Divider>);
        renderItem.push(
          <Row gutter={24} key="top0">
            <Col span={1} style={{ textAlign: 'center' }}>
              序号
            </Col>
            <Col span={1} style={{ textAlign: 'center' }}>
              姓名
            </Col>
            <Col span={2} style={{ textAlign: 'center' }}>
              姓名读音
            </Col>
            <Col span={2} style={{ textAlign: 'center' }}>
              手机号码
            </Col>
            <Col span={2} style={{ textAlign: 'center' }}>
              移动运营商
            </Col>
            <Col span={2} style={{ textAlign: 'center' }}>
              银行卡号
            </Col>
            <Col span={3} style={{ textAlign: 'center' }}>
              银行分行
            </Col>
            <Col span={2} style={{ textAlign: 'center' }}>
              银行编码
            </Col>
            <Col span={2} style={{ textAlign: 'center' }}>
              身份证号码
            </Col>
            <Col span={2} style={{ textAlign: 'center' }}>
              成功充值
            </Col>
            <Col span={1} style={{ textAlign: 'center' }}>
              性别
            </Col>
            <Col span={1} style={{ textAlign: 'center' }}>
              年龄
            </Col>
          </Row>
        );
        for (let index = 0; index < result.length; index += 1) {
          const resultItem = result[index];
          renderItem.push(
            <Row gutter={24} key={index}>
              <Col span={1} style={{ textAlign: 'center' }}>
                {index + 1}
              </Col>
              <Col span={1} style={{ textAlign: 'center' }}>
                {resultItem['姓名']}
              </Col>
              <Col span={2} style={{ textAlign: 'center' }}>
                {resultItem['姓名读音']}
              </Col>
              <Col span={2} style={{ textAlign: 'center' }}>
                {resultItem['手机号码']}
              </Col>
              <Col span={2} style={{ textAlign: 'center' }}>
                {resultItem['移动运营商']}
              </Col>
              <Col span={2} style={{ textAlign: 'center' }}>
                {resultItem['银行卡号']}
              </Col>
              <Col span={3} style={{ textAlign: 'center' }}>
                {resultItem['银行分行']}
              </Col>
              <Col span={2} style={{ textAlign: 'center' }}>
                {resultItem['银行编码']}
              </Col>
              <Col span={2} style={{ textAlign: 'center' }}>
                {resultItem['身份证号码']}
              </Col>
              <Col span={2} style={{ textAlign: 'center' }}>
                {resultItem['成功充值']}
              </Col>
              <Col span={1} style={{ textAlign: 'center' }}>
                {resultItem['性别']}
              </Col>
              <Col span={1} style={{ textAlign: 'center' }}>
                {resultItem['年龄']}
              </Col>
            </Row>
          );
        }
      }
    }

    if (RaMessage !== '') {
      renderItem.push(<Divider key="DividerRegisterAll4">文本结果</Divider>);
      renderItem.push(
        <Row gutter={24} key="RegisterAllRow6">
          <Col span={24} style={{ textAlign: 'center' }}>
            {RaMessage}
          </Col>
        </Row>
      );
    }
    return renderItem;
  }

  renderSwitch() {
    const renderItem = [];
    const { niu } = this.props;
    const { Hosts, SwitchMessage } = niu;

    if (SwitchMessage !== '') {
      renderItem.push(<Divider key="DividerOpenCodeRow0">执行结果</Divider>);
      renderItem.push(
        <Row gutter={24} key="OpenCodeRowMsg0">
          <Col span={24} style={{ textAlign: 'center' }}>
            {SwitchMessage}
          </Col>
        </Row>
      );
    }

    renderItem.push(
      <Row gutter={24} key="OpenCodeRowTop0">
        <Col span={1} style={{ textAlign: 'center' }}>
          <b>序号</b>
        </Col>
        <Col span={2} style={{ textAlign: 'center' }}>
          <b>环境地址</b>
        </Col>
        <Col span={2} style={{ textAlign: 'center' }}>
          <b>环境代号</b>
        </Col>
        <Col span={2} style={{ textAlign: 'center' }}>
          <b>工程名称</b>
        </Col>
        <Col span={3} style={{ textAlign: 'center' }}>
          <b>域名</b>
        </Col>
        <Col span={4} style={{ textAlign: 'center' }}>
          <b>官网验证码</b>
        </Col>
        <Col span={4} style={{ textAlign: 'center' }}>
          <b>BE万能验证码</b>
        </Col>
        <Col span={4} style={{ textAlign: 'center' }}>
          <b>BEAdmin权限</b>
        </Col>
        <Col span={2} style={{ textAlign: 'center' }}>
          <b>操作状态</b>
        </Col>
      </Row>
    );
    for (let index = 0; index < Hosts.length; index += 1) {
      const host = Hosts[index];
      const ipArray = host.ip.split('.');
      const ipEnd = ipArray[3];
      const envName = ipEnd.substr(-3, ipEnd.length - 1);
      const { project_name: projectName } = host;
      const ipSwitch = `${ipArray[0]}.${ipArray[1]}.${ipArray[2]}.${ipEnd.substr(
        -3,
        ipEnd.length - 1
      )}4`;

      renderItem.push(
        <Row gutter={24} key={`OpenCodeRow${index}`}>
          <Col span={1} style={{ textAlign: 'center' }}>
            {index + 1}
          </Col>
          <Col span={2} style={{ textAlign: 'center' }}>
            {host.ip}
          </Col>
          <Col span={2} style={{ textAlign: 'center' }}>{`${envName}X段环境`}</Col>
          <Col span={2} style={{ textAlign: 'center' }}>
            {projectName}
          </Col>
          <Col span={3} style={{ textAlign: 'center' }}>
            {host.name}
          </Col>
          <Col span={4} style={{ textAlign: 'center' }}>
            <Switch
              key={`Switch${index}`}
              checkedChildren="强制启用"
              unCheckedChildren="状态未知"
              defaultChecked={false}
              onChange={this.onSwitchOn('user_data', 'open-code', ipSwitch)}
            />
          </Col>
          <Col span={4} style={{ textAlign: 'center' }}>
            <Switch
              key={`Switch${index}`}
              checkedChildren="强制启用"
              unCheckedChildren="状态未知"
              defaultChecked={false}
              onChange={this.onSwitchOn('product_data', 'be-code', ipSwitch)}
            />
          </Col>
          <Col span={4} style={{ textAlign: 'center' }}>
            <Switch
              key={`Switch${index}`}
              checkedChildren="强制启用"
              unCheckedChildren="状态未知"
              defaultChecked={false}
              onChange={this.onSwitchOn('product_data', 'be-admin', ipSwitch)}
            />
          </Col>
          <Col span={2} style={{ textAlign: 'center' }}>
            &nbsp;
          </Col>
        </Row>
      );
    }
    return renderItem;
  }

  renderUserData() {
    const renderItem = [];
    const { niu } = this.props;
    const { UserData } = niu;
    const { userCount } = this.state;

    for (let index = 0; index < UserData.length; index += 1) {
      const user = UserData[index];
      const {
        name,
        sex,
        age,
        name_pinyin: namePinyin,
        id_card: idCard,
        birthday,
        mobile,
        bank_name: bankName,
        bank_card: bankCard,
        mobile_operators: mobileOperators,
        email,
        origin,
      } = user;
      renderItem.push(
        <Divider key={`Divider${index}`} orientation="left">{`${user.key} : ${user.name}`}</Divider>
      );
      renderItem.push(
        <Row gutter={24} key={`row${4 * index}${0}`}>
          <Col span={3} style={{ textAlign: 'right' }}>
            姓名
          </Col>
          <Col span={4} style={{ textAlign: 'left' }}>
            {name}
          </Col>
          <Col span={3} style={{ textAlign: 'right' }}>
            性别
          </Col>
          <Col span={4} style={{ textAlign: 'left' }}>
            {sex}
          </Col>
          <Col span={3} style={{ textAlign: 'right' }}>
            年龄
          </Col>
          <Col span={4} style={{ textAlign: 'left' }}>
            {age}
          </Col>
        </Row>
      );

      renderItem.push(
        <Row gutter={24} key={`row${4 * index}${1}`}>
          <Col span={3} style={{ textAlign: 'right' }}>
            姓名读音
          </Col>
          <Col span={4} style={{ textAlign: 'left' }}>
            {namePinyin}
          </Col>
          <Col span={3} style={{ textAlign: 'right' }}>
            身份证号码
          </Col>
          <Col span={4} style={{ textAlign: 'left' }}>
            {idCard}
          </Col>
          <Col span={3} style={{ textAlign: 'right' }}>
            出生日期
          </Col>
          <Col span={4} style={{ textAlign: 'left' }}>
            {birthday}
          </Col>
        </Row>
      );

      renderItem.push(
        <Row gutter={24} key={`row${4 * index}${2}`}>
          <Col span={3} style={{ textAlign: 'right' }}>
            手机号码
          </Col>
          <Col span={4} style={{ textAlign: 'left' }}>
            {mobile}
          </Col>
          <Col span={3} style={{ textAlign: 'right' }}>
            银行分行
          </Col>
          <Col span={4} style={{ textAlign: 'left' }}>
            {bankName}
          </Col>
          <Col span={3} style={{ textAlign: 'right' }}>
            银行卡号
          </Col>
          <Col span={4} style={{ textAlign: 'left' }}>
            {bankCard}
          </Col>
        </Row>
      );

      renderItem.push(
        <Row gutter={24} key={`row${4 * index}${3}`}>
          <Col span={3} style={{ textAlign: 'right' }}>
            移动运营商
          </Col>
          <Col span={4} style={{ textAlign: 'left' }}>
            {mobileOperators}
          </Col>
          <Col span={3} style={{ textAlign: 'right' }}>
            电子邮箱
          </Col>
          <Col span={4} style={{ textAlign: 'left' }}>
            {email}
          </Col>
          <Col span={3} style={{ textAlign: 'right' }}>
            籍贯
          </Col>
          <Col span={4} style={{ textAlign: 'left' }}>
            {origin}
          </Col>
        </Row>
      );
    }

    renderItem.push(<Divider key="DividerBtn0">^-^</Divider>);

    renderItem.push(
      <Row gutter={24} key="rowbtn0">
        <Col span={7} style={{ textAlign: 'right' }}>
          <Button
            htmlType="button"
            key="btn_1"
            type="primary"
            onClick={this.onRefreshUserDataChange(userCount)}
          >
            刷新
          </Button>
        </Col>
        <Col span={15} style={{ textAlign: 'left' }}>
          <Button
            htmlType="button"
            key="btn_1"
            type="dashed"
            onClick={this.onRefreshUserDataChange(1)}
          >
            刷新(1条)
          </Button>
          <Button
            htmlType="button"
            key="btn_2"
            type="dashed"
            onClick={this.onRefreshUserDataChange(2)}
          >
            刷新(2条)
          </Button>
          <Button
            htmlType="button"
            key="btn_3"
            type="dashed"
            onClick={this.onRefreshUserDataChange(3)}
          >
            刷新(3条)
          </Button>
          <Button
            htmlType="button"
            key="btn_5"
            type="dashed"
            onClick={this.onRefreshUserDataChange(5)}
          >
            刷新(5条)
          </Button>
          <Button
            htmlType="button"
            key="btn_10"
            type="dashed"
            onClick={this.onRefreshUserDataChange(10)}
          >
            刷新(10条)
          </Button>
        </Col>
      </Row>
    );

    return renderItem;
  }

  renderTestSuite = tcSuites => {
    const jsxTabPane = [];

    if (tcSuites === undefined) {
      return '';
    }

    Object.keys(tcSuites).forEach(tsKey => {
      const { testcases } = tcSuites[tsKey];
      jsxTabPane.push(<Divider key={`DividerTestSuite${tsKey}`}>测试套{tsKey}</Divider>);
      jsxTabPane.push(
        <Table
          key={`table${tsKey}`}
          dataSource={testcases}
          columns={tcColumns}
          pagination={{
            // 分页
            total: 100, // 数据总数量
            position: 'both',
            size: 'small',
            pageSize: 100, // 显示几条一页
            defaultPageSize: 100, // 默认显示几条一页
            pageSizeOptions: ['5', '10', '20', '50', '100'],
            showQuickJumper: true,
            hideOnSinglePage: true,
            showSizeChanger: true,
            // showTotal: function(total) {
            //   return '共 ' + total + ' 条数据';
            // }
          }}
        />
      );
    });

    return jsxTabPane;
  };

  renderJobStep(taskKey) {
    const jsxJob = [];
    const { tasks } = this.state;
    const { jobs } = tasks[taskKey];
    Object.keys(jobs).forEach(jobKey => {
      const { jobTitle, jobDescription, jobStatus } = jobs[jobKey];
      jsxJob.push(
        <Step
          key={jobKey}
          title={jobTitle}
          description={jobDescription}
          status={jobStatus}
          icon={NiuPage.renderStepIcon(jobStatus)}
        />
      );
    });
    return jsxJob;
  }

  static renderStepIcon(jobStatus) {
    if (jobStatus === 'finish') {
      return <Icon type="check-circle" theme="twoTone" />;
    }
    if (jobStatus === 'process') {
      return <Icon type="sync" spin />;
    }
    if (jobStatus === 'wait') {
      return <Icon type="smile" theme="outlined" />;
    }
    if (jobStatus === 'error') {
      return <Icon type="close-circle" theme="twoTone" />;
    }

    return <Icon type="close-circle" theme="twoTone" />;
  }

  renderJobPanel(taskKey) {
    const jsxJobPanel = [];
    const { tasks } = this.state;
    const { jobs } = tasks[taskKey];

    Object.keys(jobs).forEach(jobKey => {
      const { jobTitle: jobHeader, jobDescription, testsuites: testSuites, jobStatus } = jobs[
        jobKey
      ];
      const panelHeader = (
        <div>
          {NiuPage.renderStepIcon(jobStatus)}
          {jobHeader}
          {jobDescription}
        </div>
      );
      jsxJobPanel.push(
        <Panel header={panelHeader} key={jobKey} showArrow>
          {this.renderTestSuite(testSuites)}
        </Panel>
      );
    });
    return jsxJobPanel;
  }

  renderTask() {
    const jsxTabPanel = [];
    const { tasks } = this.state;

    if (tasks === undefined || tasks == null) {
      jsxTabPanel.push(
        <TabPane tab="." key="tabP000">
          .
        </TabPane>
      );
    } else {
      Object.keys(tasks).forEach(taskKey => {
        const task = tasks[taskKey];
        const { taskTitle } = task;
        const { defaultActiveKey } = tasks[taskKey];

        jsxTabPanel.push(
          <TabPane tab={taskTitle} key={taskKey}>
            <Divider key="DividerOutput0" orientation="right">
              .
            </Divider>
            <Steps current={0} size="small" status="process" direction="horizontal">
              {this.renderJobStep(taskKey)}
            </Steps>
            <Divider key="DividerOutput1" orientation="right">
              .
            </Divider>
            <Collapse defaultActiveKey={defaultActiveKey}>{this.renderJobPanel(taskKey)}</Collapse>
          </TabPane>
        );
      });
    }

    return jsxTabPanel;
  }

  render() {
    const { inputWindowDisplay, outputWindowDisplay, outputActiveKey } = this.state;
    return (
      <PageHeaderWrapper>
        <Tabs
          key="inputTab"
          tabPosition="top"
          activeKey={outputActiveKey}
          style={{ display: inputWindowDisplay }}
          onChange={this.onInputTabChange}
        >
          <TabPane tab="随机用户信息" key="1">
            {this.renderUserData()}
          </TabPane>
          <TabPane tab="生成用户数据" key="ra">
            {this.renderRegisterAll()}
          </TabPane>
          <TabPane tab="录入资产" key="loan">
            {this.renderLoan()}
          </TabPane>
          <TabPane tab="发散标产品" key="single">
            {this.renderSingle()}
          </TabPane>
          <TabPane tab="环境开关" key="switch">
            {this.renderSwitch()}
          </TabPane>
        </Tabs>
        <Tabs
          activeKey={outputActiveKey}
          size="small"
          onChange={this.onTaskChange}
          tabPosition="left"
          style={{ display: outputWindowDisplay }}
          key="taskTab"
        >
          {this.renderTask()}
        </Tabs>
      </PageHeaderWrapper>
    );
  }
}

export default NiuPage;
