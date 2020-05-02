import React, { Component } from 'react';
import { connect } from 'dva';
import {
  Card,
  Tabs,
  DatePicker,
  Divider,
  Row,
  Col,
  Table,
  Popconfirm,
  Button,
  Modal,
  Select,
  message,
} from 'antd';
import { TimelineChart, Pie } from '@/components/Charts';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import { getTimeDistance } from '@/utils/utils';
import styles from './analysis.less';
import { AsyncLoadBizCharts } from '@/components/Charts/AsyncLoadBizCharts';

const { TabPane } = Tabs;
const { RangePicker } = DatePicker;
const { Option } = Select;

@connect(({ user, chart, project, environment, loading }) => ({
  chart,
  currentUser: user.currentUser,
  teams: project.teams,
  server: environment.envList.data || [],
  envLoading: loading.effects['environment/fetchEnv'],
  loading: loading.effects['chart/fetchTestData'],
  loadingDocker: loading.effects['chart/fetchDocker'],
}))
class AutoTestAnalysis extends Component {
  state = {
    rangePickerValue: getTimeDistance('year'),
    currentTabKey: 'gui',
    reportsKey: '',
    env: undefined,
    type: 'WEB',
    visible: false,
  };

  componentDidMount() {
    const { dispatch } = this.props;
    const { currentTabKey, rangePickerValue } = this.state;
    this.reqRef = requestAnimationFrame(() => {
      dispatch({
        type: 'chart/fetchTestData',
        op: currentTabKey,
        action: 'case',
        payload: {
          startTime: rangePickerValue[0].format('YYYY-MM-DD'),
          endTime: rangePickerValue[1].format('YYYY-MM-DD'),
        },
      });
      dispatch({
        type: 'chart/fetchTestData',
        op: currentTabKey,
        action: 'case',
        payload: {
          startTime: rangePickerValue[0].format('YYYY-MM-DD'),
          endTime: rangePickerValue[1].format('YYYY-MM-DD'),
          status: true,
        },
      });
      dispatch({
        type: 'chart/fetchTestData',
        op: currentTabKey,
        action: 'reports',
        payload: {
          startTime: rangePickerValue[0].format('YYYY-MM-DD'),
          endTime: rangePickerValue[1].format('YYYY-MM-DD'),
        },
      });
      dispatch({
        type: 'chart/fetchDocker',
        op: 'runtime',
        action: 'list',
      });
      dispatch({
        type: 'project/fetchTeams',
        payload: {
          type: 'teams',
        },
      });
    });
  }

  componentWillUnmount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'chart/clear',
    });
    cancelAnimationFrame(this.reqRef);
  }

  handleRangePickerChange = rangePickerValue => {
    const { dispatch } = this.props;
    const { currentTabKey, reportsKey } = this.state;
    this.setState({
      rangePickerValue,
    });
    dispatch({
      type: 'chart/fetchTestData',
      op: currentTabKey,
      action: 'case',
      payload: {
        startTime: rangePickerValue[0].format('YYYY-MM-DD'),
        endTime: rangePickerValue[1].format('YYYY-MM-DD'),
      },
    });
    dispatch({
      type: 'chart/fetchTestData',
      op: currentTabKey,
      action: 'case',
      payload: {
        startTime: rangePickerValue[0].format('YYYY-MM-DD'),
        endTime: rangePickerValue[1].format('YYYY-MM-DD'),
        status: true,
      },
    });
    dispatch({
      type: 'chart/fetchTestData',
      op: currentTabKey,
      action: 'reports',
      payload: {
        startTime: rangePickerValue[0].format('YYYY-MM-DD'),
        endTime: rangePickerValue[1].format('YYYY-MM-DD'),
        key: reportsKey,
      },
    });
  };

  handleTabChange = key => {
    const { dispatch } = this.props;
    const { rangePickerValue } = this.state;
    this.setState({
      currentTabKey: key,
      reportsKey: '',
    });
    dispatch({
      type: 'chart/fetchTestData',
      op: key,
      action: 'case',
      payload: {
        startTime: rangePickerValue[0].format('YYYY-MM-DD'),
        endTime: rangePickerValue[1].format('YYYY-MM-DD'),
      },
    });
    dispatch({
      type: 'chart/fetchTestData',
      op: key,
      action: 'case',
      payload: {
        startTime: rangePickerValue[0].format('YYYY-MM-DD'),
        endTime: rangePickerValue[1].format('YYYY-MM-DD'),
        status: true,
      },
    });
    dispatch({
      type: 'chart/fetchTestData',
      op: key,
      action: 'reports',
      payload: {
        startTime: rangePickerValue[0].format('YYYY-MM-DD'),
        endTime: rangePickerValue[1].format('YYYY-MM-DD'),
      },
    });
  };

  handleJobsTabChange = (op, key) => {
    const { dispatch } = this.props;
    const { rangePickerValue } = this.state;
    this.setState({
      currentTabKey: op,
      reportsKey: key,
    });
    dispatch({
      type: 'chart/fetchTestData',
      op,
      action: 'case',
      payload: {
        startTime: rangePickerValue[0].format('YYYY-MM-DD'),
        endTime: rangePickerValue[1].format('YYYY-MM-DD'),
      },
    });
    dispatch({
      type: 'chart/fetchTestData',
      op,
      action: 'case',
      payload: {
        startTime: rangePickerValue[0].format('YYYY-MM-DD'),
        endTime: rangePickerValue[1].format('YYYY-MM-DD'),
        satus: true,
      },
    });
    dispatch({
      type: 'chart/fetchTestData',
      op,
      action: 'reports',
      payload: {
        startTime: rangePickerValue[0].format('YYYY-MM-DD'),
        endTime: rangePickerValue[1].format('YYYY-MM-DD'),
        key,
      },
    });
  };

  selectDate = type => {
    const { dispatch } = this.props;
    const { currentTabKey, reportsKey } = this.state;
    this.setState({
      rangePickerValue: getTimeDistance(type),
    });
    dispatch({
      type: 'chart/fetchTestData',
      op: currentTabKey,
      action: 'case',
      payload: {
        startTime: getTimeDistance(type)[0].format('YYYY-MM-DD'),
        endTime: getTimeDistance(type)[1].format('YYYY-MM-DD'),
      },
    });
    dispatch({
      type: 'chart/fetchTestData',
      op: currentTabKey,
      action: 'case',
      payload: {
        startTime: getTimeDistance(type)[0].format('YYYY-MM-DD'),
        endTime: getTimeDistance(type)[1].format('YYYY-MM-DD'),
        status: true,
      },
    });
    dispatch({
      type: 'chart/fetchTestData',
      op: currentTabKey,
      action: 'reports',
      payload: {
        startTime: getTimeDistance(type)[0].format('YYYY-MM-DD'),
        endTime: getTimeDistance(type)[1].format('YYYY-MM-DD'),
        key: reportsKey,
      },
    });
  };

  deleteDocker = (jobId, dockerId) => {
    const { dispatch } = this.props;
    dispatch({
      type: 'jobs/runJenkins',
      op: 'delete',
      payload: {
        jobId,
        dockerId,
      },
      callback: ()=>{
        dispatch({
          type: 'chart/fetchDocker',
          op: 'runtime',
          action: 'list',
        });
      },
    });
  };

  createDriver = () => {
    const { dispatch } = this.props;
    dispatch({
      type: 'environment/fetchEnv',
      op: 'server',
      action: 'all',
    });
    this.setState({
      visible: true,
    });
  };

  getOption = list => {
    if (!list || list.length < 1) {
      return (
        <Option key={0} value={0}>
          没有找到选项
        </Option>
      );
    }
    return list.map(item => (
      <Option key={item.key} value={item.id} title={item.description}>
        {item.title}
      </Option>
    ));
  };

  selectServer = item => {
    this.setState({ env: item });
  };

  selectTest = item => {
    this.setState({ type: item });
  };

  handleOk = () => {
    const { dispatch } = this.props;
    const { env, type } = this.state;
    if (env && type) {
      dispatch({
        type: 'jobs/runJenkins',
        op: 'env',
        payload: {
          envId: env,
          testType: type,
        },
      });
      this.setState({
        visible: false,
      });
    } else {
      message.error('请测试环境和测试类型!');
    }
  };

  handleCancel = () => {
    this.setState({
      visible: false,
    });
  };

  isActive(type) {
    const { rangePickerValue } = this.state;
    const value = getTimeDistance(type);
    if (!rangePickerValue[0] || !rangePickerValue[1]) {
      return '';
    }
    if (
      rangePickerValue[0].isSame(value[0], 'day') &&
      rangePickerValue[1].isSame(value[1], 'day')
    ) {
      return styles.currentDate;
    }
    return '';
  }

  render() {
    const { rangePickerValue, currentTabKey, reportsKey, env, visible, type } = this.state;
    const { chart, teams, loading, currentUser, loadingDocker, server, envLoading } = this.props;
    const {
      guiCaseData,
      apiCaseData,
      caseStatus,
      guiJobs,
      apiJobs,
      guiReports,
      apiReports,
      dockerList,
      guiJacoco,
      apiJacoco,
    } = chart;
    const salesExtra = (
      <div className={styles.salesExtraWrap}>
        <div className={styles.salesExtra}>
          <a className={this.isActive('today')} onClick={() => this.selectDate('today')}>
            今日
          </a>
          <a className={this.isActive('week')} onClick={() => this.selectDate('week')}>
            本周
          </a>
          <a className={this.isActive('month')} onClick={() => this.selectDate('month')}>
            本月
          </a>
          <a className={this.isActive('year')} onClick={() => this.selectDate('year')}>
            全年
          </a>
          <a className={this.isActive('all')} onClick={() => this.selectDate('all')}>
            全部
          </a>
        </div>
        <RangePicker
          allowClear={false}
          value={rangePickerValue}
          onChange={this.handleRangePickerChange}
          style={{ width: 256 }}
        />
      </div>
    );

    const guiCel = teams
      .filter(item => Object.keys(guiCaseData).includes(item.tid.toString()))
      .map(item => (
        <Col key={item.tid} span={8}>
          <Pie
            title={item.name}
            subTitle="用例总数"
            total={() => (
              <span
                // eslint-disable-next-line react/no-danger
                dangerouslySetInnerHTML={{
                  __html:
                    guiCaseData[item.tid] &&
                    guiCaseData[item.tid].reduce((pre, now) => now.y + pre, 0),
                }}
              />
            )}
            data={guiCaseData[item.tid]}
            height={280}
          />
        </Col>
      ));
    const apiCel = teams
      .filter(item => Object.keys(apiCaseData).includes(item.tid.toString()))
      .map(item => (
        <Col key={item.tid} span={8}>
          <Pie
            title={item.name}
            subTitle="用例总数"
            subTitleTwo="接口总数"
            total={() => (
              <span
                // eslint-disable-next-line react/no-danger
                dangerouslySetInnerHTML={{
                  __html:
                    apiCaseData[item.tid] &&
                    apiCaseData[item.tid].reduce((pre, now) => now.y + pre, 0),
                }}
              />
            )}
            totalTwo={() => (
              <span
                // eslint-disable-next-line react/no-danger
                dangerouslySetInnerHTML={{
                  __html:
                    apiCaseData[item.tid] &&
                    apiCaseData[item.tid].reduce((pre, now) => now.z + pre, 0),
                }}
              />
            )}
            data={apiCaseData[item.tid]}
            height={280}
          />
        </Col>
      ));
    const statusCel = teams
      .filter(item => Object.keys(caseStatus).includes(item.tid.toString()))
      .map(item => (
        <Col key={item.tid} span={8}>
          <Pie
            hasLegend
            title={item.name}
            subTitle="实现率"
            total={() => (
              <span
                // eslint-disable-next-line react/no-danger
                dangerouslySetInnerHTML={{
                  __html:
                    caseStatus[item.tid] &&
                    (
                      (caseStatus[item.tid].reduce(
                        (pre, now) => now.x === '已实现' && now.y + pre,
                        0
                      ) /
                        caseStatus[item.tid].reduce((pre, now) => now.y + pre, 0)) *
                      100
                    )
                      .toFixed(2)
                      .concat('%'),
                }}
              />
            )}
            data={caseStatus[item.tid]}
            height={240}
          />
        </Col>
      ));

    const columns = [
      {
        title: '#',
        dataIndex: 'key',
        key: 'key',
        width: '4%',
        render: text => text,
      },
      {
        title: '任务/环境编号',
        dataIndex: 'jid',
        key: 'jid',
        width: '12%',
        render: text => text,
      },
      {
        title: '任务/环境名称',
        dataIndex: 'title',
        key: 'title',
        width: '15%',
        render: text => text,
      },
      {
        title: 'DOCKER容器编号',
        dataIndex: 'id',
        key: 'id',
        width: '15%',
        render: text => text,
      },
      {
        title: 'DOCKER容器名称',
        dataIndex: 'name',
        key: 'name',
        width: '15%',
        render: text => text,
      },
      {
        title: '服务地址',
        dataIndex: 'url',
        key: 'url',
        width: '20%',
        render: text =>
          text && (
            <a href={text} target="_blank" rel="noopener noreferrer">
              {text}
            </a>
          ),
      },
      {
        title: '类型',
        dataIndex: 'type',
        key: 'type',
        width: '10%',
        render: text => text || '系统创建',
      },
      {
        title: '操作',
        key: 'action',
        render: (_, record) => {
          if (currentUser.authority === 'admin' || currentUser.userId === record.userId) {
            return (
              <Popconfirm
                title="删除运行时DOCKER会导致测试中断, 是否要删除？"
                onConfirm={() => this.deleteDocker(record.jid, record.id)}
              >
                <a>删除</a>
              </Popconfirm>
            );
          }
          return '无权限';
        },
      },
    ];

    return (
      <PageHeaderWrapper>
        <Card
          title="运行时环境管理"
          bordered={false}
          style={{ marginBottom: 32 }}
          loading={loadingDocker}
          extra={
            <Button
              icon="plus"
              type="primary"
              onClick={() => {
                this.createDriver();
              }}
            >
              新建调试环境
            </Button>
          }
        >
          <Table
            columns={columns}
            dataSource={dockerList}
            pagination={{
              showSizeChanger: true,
              showQuickJumper: true,
              hideOnSinglePage: true,
              total: dockerList.length,
              showTotal: () => '共 '.concat(dockerList.length).concat(' 条'),
            }}
          />
        </Card>
        <Card loading={loading} bordered={false} bodyStyle={{ padding: 0 }}>
          <div className={styles.salesCard}>
            <Tabs
              activeKey={currentTabKey}
              onChange={this.handleTabChange}
              size="large"
              tabBarStyle={{ marginBottom: 24 }}
              tabBarExtraContent={salesExtra}
            >
              <TabPane tab="GUI自动化测试" key="gui">
                <Card title="测试用例汇总" bordered={false}>
                  <Row>{guiCel}</Row>
                  <Row>{statusCel}</Row>
                </Card>
                <Divider />
                <Card title="测试结果汇总" bordered={false}>
                  <Tabs
                    activeKey={reportsKey || (guiJobs[0] && guiJobs[0].id)}
                    onChange={e => this.handleJobsTabChange('gui', e)}
                  >
                    {guiJobs.map(item => (
                      <TabPane tab={item.name} key={item.id}>
                        <div style={{ padding: '0 24px' }}>
                          <center><h3>测试用例执行趋势图</h3></center>
                          <TimelineChart
                            height={500}
                            data={guiReports}
                            titleMap={{
                              y1: '执行用例数',
                              y2: '通过用例数',
                              y3: '通过率 (%)',
                              y4: '执行率 (%)',
                            }}
                          />
                          <Divider />
                          <center><h3>测试覆盖率趋势图 (%)</h3></center>
                          <TimelineChart
                            height={500}
                            data={guiJacoco}
                            titleMap={{
                              y1: 'LINE',
                              y2: 'BRANCH',
                              y3: 'METHOD',
                              y4: 'CLASS',
                            }}
                          />
                        </div>
                      </TabPane>
                    ))}
                  </Tabs>
                </Card>
              </TabPane>
              <TabPane tab="API自动化测试" key="api">
                <Card title="测试用例汇总" bordered={false}>
                  <Row>{apiCel}</Row>
                  <Row>{statusCel}</Row>
                </Card>
                <Divider />
                <Card title="测试结果汇总" bordered={false}>
                  <Tabs
                    activeKey={reportsKey || (apiJobs[0] && apiJobs[0].id)}
                    onChange={e => this.handleJobsTabChange('api', e)}
                  >
                    {apiJobs.map(item => (
                      <TabPane tab={item.name} key={item.id}>
                        <div style={{ padding: '0 24px' }}>
                          <center><h3>测试用例执行趋势图</h3></center>
                          <TimelineChart
                            height={500}
                            data={apiReports}
                            titleMap={{
                              y1: '执行用例数',
                              y2: '通过用例数',
                              y3: '通过率 (%)',
                              y4: '执行率 (%)',
                            }}
                          />
                          <Divider />
                          <center><h3>测试覆盖率趋势图 (%)</h3></center>
                          <TimelineChart
                            height={500}
                            data={apiJacoco}
                            titleMap={{
                              y1: 'LINE',
                              y2: 'BRANCH',
                              y3: 'METHOD',
                              y4: 'CLASS',
                            }}
                          />
                        </div>
                      </TabPane>
                    ))}
                  </Tabs>
                </Card>
              </TabPane>
            </Tabs>
          </div>
        </Card>
        <Modal
          title="新建调试环境(24小时后自动销毁)"
          visible={visible}
          onOk={() => this.handleOk()}
          confirmLoading={envLoading}
          onCancel={this.handleCancel}
          width={500}
        >
          <Row style={{ marginBottom: 20 }}>
            <Col span={6} style={{ textAlign: 'right', paddingRight: 20 }}>
              <span>测试环境:</span>
            </Col>
            <Col span={18}>
              <Select
                style={{ width: 300 }}
                value={env}
                placeholder="请选择测试环境"
                onSelect={this.selectServer}
              >
                {this.getOption(server)}
              </Select>
            </Col>
          </Row>
          <Row style={{ marginBottom: 20 }}>
            <Col span={6} style={{ textAlign: 'right', paddingRight: 20 }}>
              <span>测试类型:</span>
            </Col>
            <Col span={18}>
              <Select
                value={type}
                placeholder="请选择测试类型"
                onSelect={this.selectTest}
                style={{ width: 300 }}
              >
                <Option key="WEB" value="WEB">
                  WEB/H5 自动化测试
                </Option>
                <Option key="DUBBO" value="DUBBO">
                  DUBBO ADMIN(DUBBO接口测试)
                </Option>
              </Select>
            </Col>
          </Row>
        </Modal>
      </PageHeaderWrapper>
    );
  }
}

export default props => (
  <AsyncLoadBizCharts>
    <AutoTestAnalysis {...props} />
  </AsyncLoadBizCharts>
);
