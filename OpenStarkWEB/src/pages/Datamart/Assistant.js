import React from 'react';
import { Divider, Input, InputNumber, Button, Row, Col, Select, Tabs } from 'antd';
import { connect } from 'dva';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';

const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

@connect(({ assistant, loading }) => ({
  assistant,
  loading,
}))
class AssistantPage extends React.Component {
  constructor(props) {
    super(props);
    this.onBtnClick = this.onBtnClick.bind(this);
    this.onSelectEnvChange = this.onSelectEnvChange.bind(this);
    this.onAccountTableParamChange = this.onAccountTableParamChange.bind(this);
    this.refreshMessage = this.refreshMessage.bind(this);
    this.initDbHost = this.initDbHost.bind(this);
    this.submitCharge = this.submitCharge.bind(this);
    this.onBtnQueryClick = this.onBtnQueryClick.bind(this);

    this.state = {
      currentEnv: '请选择测试环境',
      btnFlag: true,
      dbHost: '',
      dbUser: '',
      dbPassword: '',
      dbPort: 3306,
      postAccountTableParams: {
        userName: '',
        sqlOutput: '',
      },
      postChargeParams: {
        userName: '',
        sqlOutput: '',
        account_type: '0',
        amount: 100000,
      },
    };
  }

  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'assistant/getEnvData',
      payload: {},
    });
  }

  onSelectEnvChange(value) {
    const { dispatch } = this.props;
    const currentEnv = value;
    this.setState({
      currentEnv,
    });

    dispatch({
      type: 'assistant/getEnvData',
      payload: {
        eid: currentEnv,
        type: 'APPLICATION',
      },
    }).then(this.initDbHost);
  }

  getRndString(len) {
    const chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';
    const maxPos = chars.length;
    let pwd = '';
    for (let i = 0; i < len; i += 1) {
      pwd += chars.charAt(Math.floor(Math.random() * maxPos));
    }
    return pwd;
  }

  onBtnQueryClick = () => {
    const { dbHost, dbUser, dbPassword, dbPort } = this.state;
    const { assistant, dispatch } = this.props;
    const { userIdHashValue, userId } = assistant;

    const end8 = parseInt(userIdHashValue, 10) % 8;

    const tblAccount = `user_capital_account_${end8}`;
    const sqlQuery = `select id, balance, accountType from ${tblAccount} where userId='${userId}' and accountType in (0, 1, 2)`;
    dispatch({
      type: 'assistant/getAccountInfo',
      payload: {
        dbHost,
        dbUser,
        dbPassword,
        dbPort,
        sqlQuery,
      },
    });
  };

  onBtnClick = (cmdType, params = {}) => () => {
    const { dispatch } = this.props;
    const { dbHost, dbUser, dbPassword, dbPort  } = this.state;
    if (cmdType === 'charge') {
      const { postChargeParams } = this.state;
      const { account_type: accountType } = postChargeParams;
      const { assistant } = this.props;
      const { userIdHashValue, userId } = assistant;

      const end8 = parseInt(userIdHashValue, 10) % 8;

      const tblAccount = `user_capital_account_${end8}`;
      const sqlQuery = `select * from ${tblAccount} where userId='${userId}' and accountType='${accountType}'`;

      dispatch({
        type: 'assistant/getAccountId',
        payload: {
          dbHost,
          dbUser,
          dbPassword,
          dbPort,
          sqlQuery,
        },
      }).then(this.submitCharge);
    } else if (cmdType === 'changeUser') {
      const { userId } = params;
      dispatch({
        type: 'assistant/updateUserId',
        payload: {
          userId,
          dbHost,
          dbUser,
          dbPassword,
          dbPort,
        },
      }).then(() => {
        this.onBtnQueryClick();
      });
    } else if (cmdType === 'changeAccountTableUser') {
      const { userId } = params;
      dispatch({
        type: 'assistant/updateUserId',
        payload: {
          userId,
          dbHost,
          dbUser,
          dbPassword,
          dbPort,
        },
      });
    }
  };

  onAccountTableParamChange = paraName => eOrValue => {
    const { postAccountTableParams, dbHost, dbUser, dbPassword, dbPort  } = this.state;
    const { dispatch } = this.props;

    if (eOrValue instanceof Object) {
      if (paraName === 'userId') {
        const userId = eOrValue.target.value;
        dispatch({
          type: 'assistant/updateUserId',
          payload: { userId, dbHost, dbUser, dbPassword, dbPort },
        });
      } else if (paraName === 'userName') {
        const userName = eOrValue.target.value;
        if (dbHost !== '') {
          dispatch({
            type: 'assistant/updateUserName',
            payload: { userName, dbHost, dbUser, dbPassword, dbPort },
          }).then(this.refreshMessage);
        }
      }
    } else {
      postAccountTableParams[paraName] = eOrValue;
    }

    this.setState({
      postAccountTableParams: {
        ...postAccountTableParams,
      },
    });
  };

  onChargeParamChange = paraName => eOrValue => {
    const { postChargeParams, dbHost, dbUser, dbPassword, dbPort  } = this.state;
    const { dispatch } = this.props;
    if (eOrValue instanceof Object) {
      if (paraName === 'userId') {
        const userId = eOrValue.target.value;
        dispatch({
          type: 'assistant/updateUserId',
          payload: { userId, dbHost, dbUser, dbPassword, dbPort },
        });
        dispatch({
          type: 'assistant/getHashData',
          payload: { userId },
        });
      } else if (paraName === 'userName') {
        const userName = eOrValue.target.value;
        if (dbHost !== '') {
          dispatch({
            type: 'assistant/updateUserName',
            payload: { userName, dbHost, dbUser, dbPassword, dbPort },
          }).then(this.refreshMessage);
        }
      }
    } else {
      postChargeParams[paraName] = eOrValue;
    }

    this.setState({
      postChargeParams: {
        ...postChargeParams,
      },
    });
  };

  onRefreshClick = (cmdType, count = 24) => () => {
    const { dispatch } = this.props;
    const { dbHost, dbUser, dbPassword, dbPort } = this.state;
    if (cmdType === 'charge') {
      dispatch({
        type: 'assistant/getRandomUserList',
        payload: {
          count,
          dbHost,
          dbUser,
          dbPassword,
          dbPort,
        },
      });
    }
  };

  refreshMessage() {
    const { assistant, dispatch } = this.props;
    const { userId } = assistant;
    dispatch({
      type: 'assistant/getHashData',
      payload: { userId },
    });
  }

  submitCharge() {
    const { postChargeParams, dbHost, dbUser, dbPassword, dbPort  } = this.state;
    const { account_type: accountType, amount } = postChargeParams;
    const { assistant, dispatch } = this.props;
    const { userIdHashValue, userId, accountId } = assistant;

    const end8 = parseInt(userIdHashValue, 10) % 8;
    const tblAccount = `user_capital_account_${end8}`;
    if (accountId === '') {
      const sqlInsert = `insert into ${tblAccount}(createTime,accountType,digest,updateTime,id,userId) values(NOW(),'${accountType}','${this.getRndString(
        38
      )}',NOW(),UUID(),'${userId}')`;

      dispatch({
        type: 'assistant/insertAccount',
        payload: {
          dbHost,
          dbUser,
          dbPassword,
          dbPort,
          sqlInsert,
        },
      });

      const sqlQuery = `select * from ${tblAccount} where userId='${userId}' and accountType='${accountType}'`;

      dispatch({
        type: 'assistant/getAccountId',
        payload: {
          dbHost,
          dbUser,
          dbPassword,
          dbPort,
          sqlQuery,
        },
      }).then(this.submitCharge);
      return;
    }

    const sqlUpdate = `update ${tblAccount} set balance=balance+${amount},updateTime=NOW() where id='${accountId}';`;

    dispatch({
      type: 'assistant/updateAccount',
      payload: {
        dbHost,
        dbUser,
        dbPassword,
        dbPort,
        sqlUpdate,
      },
    }).then(this.onBtnQueryClick);
  }
  
  initDbHost() {
    const { assistant } = this.props;
    const { CurrentEnvData } = assistant;

    // 提取数据库地址
    let dbHost = '';
    for (let index = 0; index < CurrentEnvData.length; index += 1) {
      const hostItem = CurrentEnvData[index];
      const { ip, user, password, port, description } = hostItem;
      if (description.indexOf('xnaccount') > -1) {
        dbHost = ip.trim();
        this.setState({
          dbHost,
          dbUser: user,
          dbPassword: password,
          dbPort: parseInt(port, 10),
          btnFlag: false,
        });
        const { dispatch } = this.props;
        dispatch({
          type: 'assistant/getRandomUserList',
          payload: {
            count: 5,
            dbHost,
            dbUser: user,
            dbPassword: password,
            dbPort: parseInt(port, 10),
          },
        });
        break;
      }
    }
  }

  renderAccountTableMessage() {
    const renderItem = [];
    const { assistant } = this.props;
    const { AccountTableOutput, userIdHashValue, userId } = assistant;

    const end8 = parseInt(userIdHashValue, 10) % 8;
    const end32 = parseInt(userIdHashValue, 10) % 32;
    const end64 = parseInt(userIdHashValue, 10) % 64;

    // xnaccount
    let sqlOutputLocal = '# xnaccount\r\n';
    const tblAccount = `user_capital_account_${end8}`;
    sqlOutputLocal += `select * from xnaccount.${tblAccount} where userId='${userId}';\r\n`;

    const tblFundRecord = `user_fund_record_${end64}`;
    sqlOutputLocal += `select * from xnaccount.${tblFundRecord} where userId='${userId}';\r\n`;

    const tblLoanFundRecord = `loan_fund_record_${end32}`;
    sqlOutputLocal += `select * from xnaccount.${tblLoanFundRecord} where userId='${userId}';\r\n`;

    const tblLoanCapitalAccount = `loan_capital_account_${end8}`;
    sqlOutputLocal += `select * from xnaccount.${tblLoanCapitalAccount} where userId='${userId}';\r\n`;

    const tblMemberScoreRecord = `t_member_score_record_${end8}`;
    sqlOutputLocal += `select * from xnaccount.${tblMemberScoreRecord} where userId='${userId}';\r\n`;

    // pcts
    sqlOutputLocal += '# pcts\r\n';
    const tblCurrentInterestUser = `t_current_interest_user_${parseInt(userId, 10) % 64}`;
    sqlOutputLocal += `select * from pcts.${tblCurrentInterestUser} where userId='${userId}';\r\n`;

    const tblFinInvestItem = `t_fin_invest_item_${parseInt(userId, 10) % 8}`;
    sqlOutputLocal += `select * from pcts.${tblFinInvestItem} where userId='${userId}';\r\n`;

    const tblFinInvestItemTransfer = `t_fin_invest_item_transfer_${parseInt(userId, 10) % 8}`;
    sqlOutputLocal += `select * from pcts.${tblFinInvestItemTransfer} where userId='${userId}';\r\n`;

    const tblFinLoanUserRefund = `t_fin_loan_user_refund_${parseInt(userId, 10) % 8}`;
    sqlOutputLocal += `select * from pcts.${tblFinLoanUserRefund} where userId='${userId}';\r\n`;

    const tblFinLoanUserRefundCredit = `t_fin_loan_user_refund_credit_${parseInt(userId, 10) % 8}`;
    sqlOutputLocal += `select * from pcts.${tblFinLoanUserRefundCredit} where userId='${userId}';\r\n`;

    const tblFinLoanUserRefundReinvest = `t_fin_loan_user_refund_reinvest_${parseInt(userId, 10) %
      8}`;
    sqlOutputLocal += `select * from pcts.${tblFinLoanUserRefundReinvest} where userId='${userId}';\r\n`;

    const tblFlexInterestUser = `t_flex_interest_user_${parseInt(userId, 10) % 16}`;
    sqlOutputLocal += `select * from pcts.${tblFlexInterestUser} where userId='${userId}';\r\n`;

    const tblInvestRefundProduct = `t_invest_refund_product_${parseInt(userId, 10) % 16}`;
    sqlOutputLocal += `select * from pcts.${tblInvestRefundProduct} where userId='${userId}';\r\n`;

    const tblInvestRefundUser = `t_invest_refund_user_${parseInt(userId, 10) % 16}`;
    sqlOutputLocal += `select * from pcts.${tblInvestRefundUser} where userId='${userId}';\r\n`;

    const tblStandCapitalRecord = `t_stand_capital_record_${parseInt(userId, 10) % 8}`;
    sqlOutputLocal += `select * from pcts.${tblStandCapitalRecord} where userId='${userId}';\r\n`;

    const tblTransferRelationMove = `t_transfer_relation_move_${parseInt(userId, 10) % 8}`;
    sqlOutputLocal += `select * from pcts.${tblTransferRelationMove} where userId='${userId}';\r\n`;

    if (AccountTableOutput !== null) {
      renderItem.push(<Divider key="DividerAccountTable3">xnaccount</Divider>);
      renderItem.push(
        <Row gutter={24} key="AccountTableMessageRow0">
          <Col span={8} style={{ textAlign: 'right' }}>
            账户表
          </Col>
          <Col span={4} style={{ textAlign: 'left' }}>
            <Input
              size="small"
              disabled
              placeholder="账户表"
              style={{ width: 250 }}
              value={tblAccount}
              onChange={this.onAccountTableParamChange('userId')}
            />
          </Col>
          <Col span={3} style={{ textAlign: 'right' }}>
            资金表
          </Col>
          <Col span={9} style={{ textAlign: 'left' }}>
            <Input
              size="small"
              disabled
              placeholder="资金表"
              style={{ width: 250 }}
              value={tblFundRecord}
              onChange={this.onAccountTableParamChange('userId')}
            />
          </Col>
        </Row>
      );

      // 借款用户资金账户表
      renderItem.push(
        <Row gutter={24} key="AccountTableMessageRow3">
          <Col span={8} style={{ textAlign: 'right' }}>
            借款用户资金账户表
          </Col>
          <Col span={4} style={{ textAlign: 'left' }}>
            <Input
              size="small"
              disabled
              placeholder="借款用户资金账户表"
              style={{ width: 250 }}
              value={tblLoanCapitalAccount}
            />
          </Col>
          <Col span={3} style={{ textAlign: 'right' }}>
            会员成长值记录表
          </Col>
          <Col span={9} style={{ textAlign: 'left' }}>
            <Input
              size="small"
              disabled
              placeholder="会员成长值记录表"
              style={{ width: 250 }}
              value={tblMemberScoreRecord}
            />
          </Col>
        </Row>
      );

      renderItem.push(<Divider key="DividerAccountTable4">pcts</Divider>);
      // 活期计息表
      renderItem.push(
        <Row gutter={24} key="AccountTableMessageRow5">
          <Col span={8} style={{ textAlign: 'right' }}>
            活期计息表
          </Col>
          <Col span={4} style={{ textAlign: 'left' }}>
            <Input
              size="small"
              disabled
              placeholder="活期计息表"
              style={{ width: 250 }}
              value={tblCurrentInterestUser}
            />
          </Col>
          <Col span={3} style={{ textAlign: 'right' }}>
            投资债权匹配表
          </Col>
          <Col span={9} style={{ textAlign: 'left' }}>
            <Input
              size="small"
              disabled
              placeholder="投资债权匹配表"
              style={{ width: 250 }}
              value={tblFinInvestItem}
            />
          </Col>
        </Row>
      );

      // 投资债权转让表
      renderItem.push(
        <Row gutter={24} key="AccountTableMessageRow7">
          <Col span={8} style={{ textAlign: 'right' }}>
            投资债权转让表
          </Col>
          <Col span={4} style={{ textAlign: 'left' }}>
            <Input
              size="small"
              disabled
              placeholder="投资债权转让表"
              style={{ width: 250 }}
              value={tblFinInvestItemTransfer}
            />
          </Col>
          <Col span={3} style={{ textAlign: 'right' }}>
            债权用户还款明细表
          </Col>
          <Col span={9} style={{ textAlign: 'left' }}>
            <Input
              size="small"
              disabled
              placeholder="债权用户还款明细表"
              style={{ width: 250 }}
              value={tblFinLoanUserRefund}
            />
          </Col>
        </Row>
      );

      // 债权用户还款转让债权关系表
      renderItem.push(
        <Row gutter={24} key="AccountTableMessageRow9">
          <Col span={8} style={{ textAlign: 'right' }}>
            债权用户还款转让债权关系表
          </Col>
          <Col span={4} style={{ textAlign: 'left' }}>
            <Input
              size="small"
              disabled
              placeholder="债权用户还款转让债权关系表"
              style={{ width: 250 }}
              value={tblFinLoanUserRefundCredit}
            />
          </Col>
          <Col span={3} style={{ textAlign: 'right' }}>
            债权用户还款复投关系表
          </Col>
          <Col span={9} style={{ textAlign: 'left' }}>
            <Input
              size="small"
              disabled
              placeholder="债权用户还款复投关系表"
              style={{ width: 250 }}
              value={tblFinLoanUserRefundReinvest}
            />
          </Col>
        </Row>
      );

      // 升财牛用户利息表
      renderItem.push(
        <Row gutter={24} key="AccountTableMessageRow11">
          <Col span={8} style={{ textAlign: 'right' }}>
            升财牛用户利息表
          </Col>
          <Col span={4} style={{ textAlign: 'left' }}>
            <Input
              size="small"
              disabled
              placeholder="升财牛用户利息表"
              style={{ width: 250 }}
              value={tblFlexInterestUser}
            />
          </Col>
          <Col span={3} style={{ textAlign: 'right' }}>
            投资债权回款计划（产品）
          </Col>
          <Col span={9} style={{ textAlign: 'left' }}>
            <Input
              size="small"
              disabled
              placeholder="投资债权回款计划（产品）"
              style={{ width: 250 }}
              value={tblInvestRefundProduct}
            />
          </Col>
        </Row>
      );

      // 投资债权回款计划（用户）
      renderItem.push(
        <Row gutter={24} key="AccountTableMessageRow13">
          <Col span={8} style={{ textAlign: 'right' }}>
            投资债权回款计划（用户）
          </Col>
          <Col span={4} style={{ textAlign: 'left' }}>
            <Input
              size="small"
              disabled
              placeholder="投资债权回款计划（用户）"
              style={{ width: 250 }}
              value={tblInvestRefundUser}
            />
          </Col>
          <Col span={3} style={{ textAlign: 'right' }}>
            站岗资金记录表
          </Col>
          <Col span={9} style={{ textAlign: 'left' }}>
            <Input
              size="small"
              disabled
              placeholder="站岗资金记录表"
              style={{ width: 250 }}
              value={tblStandCapitalRecord}
            />
          </Col>
        </Row>
      );

      // 数据迁移转让关系表
      renderItem.push(
        <Row gutter={24} key="AccountTableMessageRow15">
          <Col span={8} style={{ textAlign: 'right' }}>
            数据迁移转让关系表
          </Col>
          <Col span={16} style={{ textAlign: 'left' }}>
            <Input
              size="small"
              disabled
              placeholder="数据迁移转让关系表"
              style={{ width: 250 }}
              value={tblTransferRelationMove}
            />
          </Col>
        </Row>
      );

      renderItem.push(<Divider key="DividerAccountTable16">辅助sql</Divider>);
      renderItem.push(
        <Row gutter={24} key="AccountTableMessageRow99">
          <Col span={8} style={{ textAlign: 'right' }}>
            {' '}
            脚本
          </Col>
          <Col span={16} style={{ textAlign: 'left' }}>
            <TextArea style={{ width: 600, height: 200 }} size="small" value={sqlOutputLocal} />
          </Col>
        </Row>
      );
    }
    return renderItem;
  }

  renderAccountTable() {
    const { btnFlag } = this.state;
    const { assistant } = this.props;
    const { userId, userName, userRandomList } = assistant;

    const renderItem = [];

    renderItem.push(<Divider key="DividerAccountTable0">测试环境</Divider>);
    renderItem.push(this.renderEnv('AccountTableEnvTop'));
    renderItem.push(<Divider key="DividerAccountTable1">业务参数</Divider>);
    renderItem.push(
      <Row gutter={24} key="AccountTableRow0">
        <Col span={8} style={{ textAlign: 'right' }}>
          用户ID
        </Col>
        <Col span={4} style={{ textAlign: 'left' }}>
          <Input
            size="small"
            placeholder="用户ID"
            style={{ width: 170 }}
            value={userId}
            disabled={btnFlag}
            onChange={this.onAccountTableParamChange('userId')}
          />
          <br />
          <label style={{ color: 'red' }}>用户ID、用户名称任选一即可</label>
        </Col>
        <Col span={2} style={{ textAlign: 'right' }}>
          用户名称
        </Col>
        <Col span={10} style={{ textAlign: 'left' }}>
          <Input
            size="small"
            placeholder="用户名称"
            style={{ width: 170 }}
            value={userName}
            disabled={btnFlag}
            onChange={this.onAccountTableParamChange('userName')}
          />
          <br />
          <label style={{ color: 'red' }}>确保输入项为对应测试环境中已存在用户！</label>
        </Col>
      </Row>
    );

    const randomItem = [];
    if (userRandomList) {
      userRandomList.forEach(user => {
        randomItem.push(
          <Button
            htmlType="button"
            key={`btn-accountTable-${user[0]}`}
            onClick={this.onBtnClick('changeAccountTableUser', { userId: user[0] })}
          >
            {user[1]}
          </Button>
        );
      });
    }
    renderItem.push(<Divider key="DividerAccountTable1_0" />);
    renderItem.push(
      <Row gutter={24} key="AccountTableRow1">
        <Col span={24} style={{ textAlign: 'center' }}>
          {randomItem}
        </Col>
      </Row>
    );
    renderItem.push(<Divider key="DividerAccountTable1_1" />);
    renderItem.push(
      <Row gutter={24} key="AccountTableRow2">
        <Col span={24} style={{ textAlign: 'center' }}>
          <Button.Group>
            <Button htmlType="button" onClick={this.onRefreshClick('charge', 5)} disabled={btnFlag}>
              刷新5条
            </Button>
            <Button
              htmlType="button"
              onClick={this.onRefreshClick('charge', 10)}
              disabled={btnFlag}
            >
              刷新10条
            </Button>
            <Button
              htmlType="button"
              onClick={this.onRefreshClick('charge', 20)}
              disabled={btnFlag}
            >
              刷新20条
            </Button>
            <Button
              htmlType="button"
              onClick={this.onRefreshClick('charge', 50)}
              disabled={btnFlag}
            >
              刷新50条
            </Button>
            <Button
              htmlType="button"
              onClick={this.onRefreshClick('charge', 100)}
              disabled={btnFlag}
            >
              刷新100条
            </Button>
          </Button.Group>
        </Col>
      </Row>
    );

    renderItem.push(this.renderAccountTableMessage());
    return renderItem;
  }

  renderChargeMessage() {
    const renderItem = [];
    const { assistant } = this.props;
    const { sqlUpdate, sqlQuery, sqlInsert, accountInfo } = assistant;

    renderItem.push(<Divider key="DividerChargeTable4">状态窗口</Divider>);

    let b1 = 0;
    let b2 = 0;
    let b3 = 0;

    for (let i = 0; i < accountInfo.length; i += 1) {
      if (accountInfo[i][2] === '0') {
        b1 = accountInfo[i][1];
      } else if (accountInfo[i][2] === '1') {
        b2 = accountInfo[i][1];
      } else if (accountInfo[i][2] === '2') {
        b3 = accountInfo[i][1];
      }
    }

    renderItem.push(
      <Row gutter={24} key="ChargeMessageRow3_0">
        <Col span={8} style={{ textAlign: 'right' }}>
          余额大类
        </Col>
        <Col span={16} style={{ textAlign: 'left' }}>
          当前数值(单位：元)
        </Col>
      </Row>
    );

    renderItem.push(
      <Row gutter={24} key="ChargeMessageRow3">
        <Col span={8} style={{ textAlign: 'right' }}>
          网贷余额
        </Col>
        <Col span={16} style={{ textAlign: 'left' }}>
          {b1}
        </Col>
      </Row>
    );

    renderItem.push(
      <Row gutter={24} key="ChargeMessageRow4">
        <Col span={8} style={{ textAlign: 'right' }}>
          理财余额
        </Col>
        <Col span={16} style={{ textAlign: 'left' }}>
          {b2}
        </Col>
      </Row>
    );
    renderItem.push(
      <Row gutter={24} key="ChargeMessageRow5">
        <Col span={8} style={{ textAlign: 'right' }}>
          基金余额
        </Col>
        <Col span={16} style={{ textAlign: 'left' }}>
          {b3}
        </Col>
      </Row>
    );

    renderItem.push(<Divider key="DividerChargeTable3">脚本</Divider>);
    renderItem.push(
      <Row gutter={24} key="ChargeMessageRow6">
        <Col span={8} style={{ textAlign: 'right' }}>
          sqlQuery
        </Col>
        <Col span={16} style={{ textAlign: 'left' }}>
          {sqlQuery}
        </Col>
      </Row>
    );

    renderItem.push(
      <Row gutter={24} key="ChargeMessageRow7">
        <Col span={8} style={{ textAlign: 'right' }}>
          {' '}
          sqlInsert
        </Col>
        <Col span={16} style={{ textAlign: 'left' }}>
          {sqlInsert}
        </Col>
      </Row>
    );

    renderItem.push(
      <Row gutter={24} key="ChargeMessageRow8">
        <Col span={8} style={{ textAlign: 'right' }}>
          {' '}
          sqlUpdate
        </Col>
        <Col span={16} style={{ textAlign: 'left' }}>
          {sqlUpdate}
        </Col>
      </Row>
    );

    return renderItem;
  }

  renderCharge() {
    const { btnFlag, postChargeParams } = this.state;
    const { account_type: accountType, amount } = postChargeParams;
    const { assistant } = this.props;
    const { userId, userName, userRandomList } = assistant;

    const renderItem = [];
    renderItem.push(<Divider key="DividerCharge0">测试环境</Divider>);
    renderItem.push(this.renderEnv('ChargeRowEnvTop'));
    renderItem.push(<Divider key="DividerCharge1">业务参数</Divider>);
    renderItem.push(
      <Row gutter={24} key="ChargeRow0">
        <Col span={8} style={{ textAlign: 'right' }}>
          用户ID
        </Col>
        <Col span={4} style={{ textAlign: 'left' }}>
          <Input
            size="small"
            placeholder="用户ID"
            style={{ width: 170 }}
            value={userId}
            disabled={btnFlag}
            onChange={this.onChargeParamChange('userId')}
          />
        </Col>
        <Col span={2} style={{ textAlign: 'right' }}>
          用户名称
        </Col>
        <Col span={10} style={{ textAlign: 'left' }}>
          <Input
            size="small"
            placeholder="用户名称"
            style={{ width: 170 }}
            value={userName}
            disabled={btnFlag}
            onChange={this.onChargeParamChange('userName')}
          />
        </Col>
      </Row>
    );
    renderItem.push(
      <Row gutter={24} key="ChargeRow1">
        <Col span={8} style={{ textAlign: 'right' }}>
          账户类型
        </Col>
        <Col span={4} style={{ textAlign: 'left' }}>
          <Select
            size="small"
            style={{ width: 170 }}
            defaultValue={accountType}
            onChange={this.onChargeParamChange('account_type')}
          >
            <Option value="0">网贷账户</Option>
            <Option value="1">理财账户</Option>
            <Option value="2">基金账户</Option>
          </Select>
        </Col>
        <Col span={2} style={{ textAlign: 'right' }}>
          充值金额
        </Col>
        <Col span={10} style={{ textAlign: 'left' }}>
          <InputNumber
            size="small"
            placeholder="充值金额"
            defaultValue={amount}
            style={{ width: 170 }}
            onChange={this.onChargeParamChange('amount')}
          />
        </Col>
      </Row>
    );

    const randomItem = [];
    if (userRandomList) {
      userRandomList.forEach(user => {
        randomItem.push(
          <Button
            htmlType="button"
            key={`btn-charge-${user[0]}`}
            onClick={this.onBtnClick('changeAccountTableUser', { userId: user[0] })}
          >
            {user[1]}
          </Button>
        );
      });
    }
    renderItem.push(<Divider key="Dividercharge1_0" />);
    renderItem.push(
      <Row gutter={24} key="ChargeRow1_0">
        <Col span={24} style={{ textAlign: 'center' }}>
          {randomItem}
        </Col>
      </Row>
    );
    renderItem.push(<Divider key="DividerCharge1_1" />);
    renderItem.push(
      <Row gutter={24} key="ChargeRow1_1">
        <Col span={24} style={{ textAlign: 'center' }}>
          <Button.Group>
            <Button htmlType="button" onClick={this.onRefreshClick('charge', 5)} disabled={btnFlag}>
              刷新5条
            </Button>
            <Button
              htmlType="button"
              onClick={this.onRefreshClick('charge', 10)}
              disabled={btnFlag}
            >
              刷新10条
            </Button>
            <Button
              htmlType="button"
              onClick={this.onRefreshClick('charge', 20)}
              disabled={btnFlag}
            >
              刷新20条
            </Button>
            <Button
              htmlType="button"
              onClick={this.onRefreshClick('charge', 50)}
              disabled={btnFlag}
            >
              刷新50条
            </Button>
            <Button
              htmlType="button"
              onClick={this.onRefreshClick('charge', 100)}
              disabled={btnFlag}
            >
              刷新100条
            </Button>
          </Button.Group>
        </Col>
      </Row>
    );

    renderItem.push(<Divider key="DividerCharge2">^-^</Divider>);
    renderItem.push(
      <Row gutter={8} key="ChargeRow2">
        <Col span={12} style={{ textAlign: 'right' }}>
          <Button
            htmlType="button"
            type="primary"
            onClick={this.onBtnQueryClick}
            disabled={btnFlag}
          >
            查询
          </Button>
        </Col>
        <Col span={12} style={{ textAlign: 'left' }}>
          <Button
            htmlType="button"
            type="primary"
            onClick={this.onBtnClick('charge')}
            disabled={btnFlag}
          >
            充值
          </Button>
        </Col>
      </Row>
    );
    renderItem.push(this.renderChargeMessage());
    return renderItem;
  }

  renderEnvOption(flagShowIp) {
    const optionList = [];
    const { assistant } = this.props;
    const { EnvData } = assistant;
    for (let index = 0; index < EnvData.length; index += 1) {
      const env = EnvData[index];
      const { key, id, title } = env;
      if (!flagShowIp) {
        if (title.indexOf('_') > -1) {
          const titleRight = String(title.split('_')[1]);
          const titleRange = String(titleRight.split('.')[3]).replace('*', 'X段环境');
          optionList.push(
            <Option value={id} key={key}>
              {titleRange}
            </Option>
          );
        } else if (title.indexOf('-') > -1) {
          const titleRight = String(title.split('-')[1]);
          const titleRange = String(titleRight.split('.')[3]).replace('*', '准生产环境');
          optionList.push(
            <Option value={id} key={key}>
              {titleRange}
            </Option>
          );
        } else {
          optionList.push(
            <Option value={id} key={key}>
              {title}
            </Option>
          );
        }
      } else if (title.indexOf('_') > -1) {
        const titleRight = String(title.split('_')[1]);
        optionList.push(
          <Option value={id} key={key}>
            {titleRight}
          </Option>
        );
      } else if (title.indexOf('-') > -1) {
        const titleRight = String(title.split('-')[1]);
        optionList.push(
          <Option value={id} key={key}>
            {titleRight}
          </Option>
        );
      } else {
        optionList.push(
          <Option value={id} key={key}>
            {title}
          </Option>
        );
      }
    }
    return optionList;
  }

  renderEnv(key) {
    const { currentEnv } = this.state;
    return (
      <Row gutter={24} key={key}>
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
  }

  render() {
    return (
      <PageHeaderWrapper>
        <Tabs key="inputTab" tabPosition="top" defaultActiveKey="charge">
          <TabPane tab="账户分表" key="account_table">
            {this.renderAccountTable()}
          </TabPane>
          <TabPane tab="资金充值" key="charge">
            {this.renderCharge()}
          </TabPane>
        </Tabs>
      </PageHeaderWrapper>
    );
  }
}

export default AssistantPage;
