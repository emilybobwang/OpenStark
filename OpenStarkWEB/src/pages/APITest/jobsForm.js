import React, { PureComponent, Fragment } from 'react';
import {
  Table,
  Button,
  Input,
  message,
  Popconfirm,
  Divider,
  Select,
  Row,
  Col,
  Pagination,
  DatePicker,
  Icon,
  Checkbox,
  Modal,
  Tag,
} from 'antd';
import moment from 'moment';
import { connect } from 'dva';
import styles from '../Tools/style.less';
import BeRunCasesForm from '../Test/BeRunCasesForm';

const { TextArea, Search } = Input;
const { Option } = Select;

@connect(({ environment, jobs, apiTest, loading }) => ({
  server: environment.envList.data || [],
  jenkinsJobs: jobs.jenkinsJobs,
  jenkinsApps: jobs.jenkinsApps,
  testCases: apiTest.testCases,
  envLoading: loading.effects['environment/fetchEnv'],
  loadingJobs: loading.effects['jobs/getJenkins'],
  caseLoading: loading.effects['apiTest/fetchApiTest'],
  jobsLoading: loading.effects['jobs/runJenkins'],
}))
class JobsForm extends PureComponent {
  index = 0;

  cacheOriginData = {};

  constructor(props) {
    super(props);

    this.state = {
      data: props.value,
      removeKeys: [],
      filters: {
        keyWord: '',
      },
      visible: false,
      name: '',
      checkedApps: [],
      selectedVersions: {},
      visibleCases: false,
      versions: {},
      pid: 0,
      exec: undefined,
      env: undefined,
      jobId: undefined,
      dayBuild: false,
      saveOnly: false,
      sendMail: true,
      mailList: [],
      clean: false,
      selectedCases: [],
      jobData: {},
    };
  }

  componentWillReceiveProps(nextProps) {
    if ('jobsList' in nextProps && nextProps.jobsList) {
      this.setState({
        data: nextProps.jobsList.data,
      });
    }
  }

  onPageChange = (page, pageSize) => {
    const { onPageChange } = this.props;
    const { filters } = this.state;
    onPageChange(page, pageSize, filters);
  };

  onShowSizeChange = (current, size) => {
    const { onPageChange } = this.props;
    const { filters } = this.state;
    onPageChange(current, size, filters);
  };

  onSearchChange = filter => {
    const { filters } = this.state;
    const keyWords = filters;
    const { onSearch } = this.props;
    if (typeof filter === 'string') {
      keyWords.keyWord = filter;
    }
    onSearch(keyWords);
    this.setState({
      filters: keyWords,
    });
  };

  onSelectChange = (selectedRowKeys, selectedRows) => {
    const { currentUser } = this.props;
    const { removeKeys } = this.state;
    const selected = selectedRows
      .filter(element => currentUser.authority === 'admin' || element.userId === currentUser.userId)
      .map(item => item.key);
    this.setState({
      removeKeys: selectedRowKeys.filter(
        item => removeKeys.indexOf(item) >= 0 || selected.indexOf(item) >= 0
      ),
    });
  };

  onSelectCases = selectedCases => {
    this.setState({ selectedCases });
  };

  getRowByKey(key, newData) {
    const { data } = this.state;
    return (newData || data).filter(item => item.key === key)[0];
  }

  beRunCases = jobData => {
    const { dispatch } = this.props;
    dispatch({
      type: 'apiTest/fetchApiTest',
      payload: {
        pid: jobData.pid,
      },
      op: 'testCase',
      action: 'list',
    });
    this.setState({
      visibleCases: true,
      name: jobData.title,
      pid: jobData.pid,
      selectedCases: jobData.selectedCases,
      jobData,
    });
  };

  onSearch = filters => {
    const { dispatch } = this.props;
    const { pid } = this.state;
    dispatch({
      type: 'apiTest/fetchApiTest',
      payload: {
        ...filters,
        pid,
      },
      op: 'testCase',
      action: 'list',
    });
  };

  handleOkCases = () => {
    const { editRows } = this.props;
    const { selectedCases, jobData } = this.state;
    if (Object.keys(jobData).length > 0) {
      jobData.selectedCases = selectedCases;
      editRows(jobData, 'edit');
      this.setState({
        visibleCases: false,
      });
    } else {
      message.error('获取当前任务信息异常!');
    }
  };

  handleCancelCases = () => {
    this.setState({
      visibleCases: false,
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

  selectExec = item => {
    this.setState({ exec: item });
  };

  selectServer = item => {
    this.setState({ env: item });
  };

  toggleEditable = (e, key) => {
    e.preventDefault();
    const { data } = this.state;
    const newData = data.map(item => ({ ...item }));
    const target = this.getRowByKey(key, newData);
    if (target) {
      // 进入编辑状态时保存原始数据
      if (!target.editable) {
        this.cacheOriginData[key] = { ...target };
      }
      target.editable = !target.editable;
      this.setState({ data: newData });
    }
  };

  removeRows = () => {
    const { editRows } = this.props;
    const { data, removeKeys, filters } = this.state;
    const newData = data.filter(item => removeKeys.indexOf(item.key) === -1);
    const rowKeys = removeKeys.filter(item => typeof item === 'number');
    this.setState({ data: newData });
    if (rowKeys.length > 0) {
      editRows({ key: rowKeys }, 'delete', () => {
        this.onSearchChange(filters);
      });
    }
    this.setState({
      removeKeys: [],
    });
  };

  newMember = () => {
    const { currentUser } = this.props;
    const { data } = this.state;
    const newData = data.map(item => ({ ...item }));
    newData.push({
      no: `NEW_TEMP_ID_${this.index}`,
      key: `NEW_TEMP_KEY_${this.index}`,
      team: '',
      tid: '',
      project: '',
      pid: '',
      title: '',
      jid: '',
      description: '',
      status: 0,
      cycle: 'once',
      planTime: new Date(),
      startTime: '',
      endTime: '',
      time: '',
      userId: currentUser.userId,
      email: [currentUser.email],
      sendMail: true,
      selectedCases: [],
      runApps: [],
      docker: [],
      editable: true,
      isNew: true,
    });
    this.index += 1;
    this.setState({ data: newData });
  };

  handleTableChange = (_, filter) => {
    const { filters } = this.state;
    const search = filters;
    if (Object.keys(filter).includes('pid')) {
      search.pid = filter.pid.join(',');
    }
    if (Object.keys(filter).includes('tid')) {
      search.tid = filter.tid.join(',');
    }
    if (Object.keys(filter).includes('status')) {
      search.status = filter.status.join(',');
    }
    this.onSearchChange(search);
  };

  startJob = (name, jobId, exec, env, runApps, email, sendMail) => {
    const { dispatch } = this.props;
    dispatch({
      type: 'environment/fetchEnv',
      op: 'server',
      action: 'all',
    });
    dispatch({
      type: 'jobs/getJenkins',
      op: 'jobs',
    });
    dispatch({
      type: 'jobs/getJenkins',
      op: 'apps',
    });
    if (runApps) {
      dispatch({
        type: 'jobs/getJenkins',
        op: 'version',
        payload: runApps.map(item => ({ apps: item })),
        callback: res => {
          const { versions, selectedVersions } = this.state;
          if (res) {
            Object.keys(res).forEach(item => {
              versions[item] = res[item];
            });
          }
          runApps.forEach(item => {
            if (Object.keys(versions).includes(item) && versions[item].length > 0) {
              selectedVersions[item] = versions[item][0].id;
            } else {
              selectedVersions[item] = 'allVersions';
            }
          });
          this.setState({ versions, selectedVersions });
        },
      });
    }
    this.setState({
      visible: true,
      name,
      jobId,
      exec: exec || undefined,
      env: env || undefined,
      checkedApps: runApps,
      mailList: email,
      sendMail,
    });
  };

  handleOk = name => {
    const { dispatch } = this.props;
    const {
      exec,
      env,
      jobId,
      filters,
      dayBuild,
      saveOnly,
      checkedApps,
      clean,
      sendMail,
      mailList,
      selectedVersions,
    } = this.state;
    if (exec && env) {
      Object.keys(selectedVersions).forEach(item => {
        if (!checkedApps.includes(item)) {
          delete selectedVersions[item];
        }
      });
      dispatch({
        type: 'jobs/runJenkins',
        op: 'jobs',
        payload: {
          exec,
          env,
          name,
          jobId,
          type: 'api',
          dayBuild,
          saveOnly,
          runApps: checkedApps,
          checkVersion: selectedVersions,
          clean,
          sendMail,
          mailList,
        },
        callback: () => {
          this.onSearchChange(filters);
        },
      });
      this.setState({
        visible: false,
      });
    } else {
      message.error('请选择执行器和测试环境!');
    }
  };

  handleCancel = () => {
    this.setState({
      visible: false,
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

  selectExec = item => {
    this.setState({ exec: item });
  };

  selectServer = item => {
    this.setState({ env: item });
  };

  runAppsOnChange = e => {
    const { dispatch } = this.props;
    const { checked, value } = e.target;
    if (checked) {
      dispatch({
        type: 'jobs/getJenkins',
        op: 'version',
        payload: {
          apps: value,
        },
        callback: res => {
          const { versions, selectedVersions } = this.state;
          if (res) {
            Object.keys(res).forEach(item => {
              versions[item] = res[item];
            });
          }
          if (
            !Object.keys(selectedVersions).includes(value) &&
            Object.keys(versions).includes(value) &&
            versions[value].length > 0
          ) {
            selectedVersions[value] = versions[value][0].id;
          } else if (!Object.keys(selectedVersions).includes(value)) {
            selectedVersions[value] = 'allVersions';
          }
          this.setState({ versions, selectedVersions });
        },
      });
    }
  };

  getVersion = (value, e) => {
    const { selectedVersions } = this.state;
    selectedVersions[e.key.split('_')[0]] = value;
    this.setState({ selectedVersions });
  };

  handleKeyPress(e, key) {
    if (e.key === 'Enter') {
      this.saveRow(e, key);
    }
  }

  handleFieldChange(e, fieldName, key) {
    const {
      project: { projectsList },
    } = this.props;
    const { data } = this.state;
    const newData = data.map(item => ({ ...item }));
    const target = this.getRowByKey(key, newData);
    if (target) {
      const tValue = e && e.target ? e.target.value : e;
      target[fieldName] = tValue;
      if (fieldName === 'pid') {
        target.project = projectsList.filter(item => item.pid === tValue)[0].name;
      }
      this.setState({
        data: newData.map(item => ({
          ...item,
          planTime: moment(item.planTime, 'YYYY-MM-DD HH:mm:ss').format('YYYY-MM-DD HH:mm:ss'),
        })),
      });
    }
  }

  remove(record) {
    const { data, removeKeys, filters } = this.state;
    const newData = data.filter(item => item.key !== record.key);
    const { editRows } = this.props;
    this.setState({ data: newData });
    if (typeof record.key === 'number') {
      editRows(record, 'delete', () => {
        this.onSearchChange(filters);
      });
    }
    this.setState({
      removeKeys: removeKeys.filter(item => item !== record.key),
    });
  }

  saveRow(e, key) {
    const { editRows } = this.props;
    e.persist();
    if (this.clickedCancel) {
      this.clickedCancel = false;
      return;
    }
    const target = this.getRowByKey(key) || {};
    if (!target.pid || !target.title || !target.planTime || !target.cycle) {
      message.error('请填写完整的任务信息。');
      e.target.focus();
      return;
    }
    this.toggleEditable(e, key);
    const { filters } = this.state;
    editRows(target, 'edit', () => {
      this.onSearchChange(filters);
    });
  }

  cancel(e, key) {
    this.clickedCancel = true;
    e.preventDefault();
    const { data } = this.state;
    const newData = data.map(item => ({ ...item }));
    const target = this.getRowByKey(key, newData);
    if (this.cacheOriginData[key]) {
      Object.assign(target, this.cacheOriginData[key]);
      target.editable = false;
      delete this.cacheOriginData[key];
    }
    this.setState({ data: newData });
    this.clickedCancel = false;
  }

  render() {
    const {
      loading,
      jobsList: { total, page },
      project: { projectsList, teams },
      currentUser,
      envLoading,
      loadingJobs,
      server,
      jenkinsJobs,
      jenkinsApps,
      testCases,
      caseLoading,
      jobsLoading,
    } = this.props;
    const option = projectsList.map(item => (
      <Option key={item.pid} value={item.pid}>
        {item.name}
      </Option>
    ));
    const columns = [
      {
        title: '#',
        dataIndex: 'no',
        key: 'no',
        width: '4%',
        render: text => text,
      },
      {
        title: '任务编号',
        dataIndex: 'jid',
        key: 'jid',
        width: '12%',
        render: text => text,
      },
      {
        title: '任务名称',
        dataIndex: 'title',
        key: 'title',
        width: '12%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                value={text}
                autoFocus
                onChange={e => this.handleFieldChange(e, 'title', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="任务名称"
              />
            );
          }
          return text;
        },
      },
      {
        title: '所属组',
        dataIndex: 'team',
        key: 'tid',
        filters: teams.map(item => ({ text: item.name, value: item.tid })),
        width: '10%',
        render: text => text,
      },
      {
        title: '所属项目',
        dataIndex: 'project',
        key: 'pid',
        filters: projectsList.map(item => ({ text: item.name, value: item.pid })),
        width: '12%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Select
                defaultValue={text}
                value={text}
                onChange={e => this.handleFieldChange(e, 'pid', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                style={{ width: '100%' }}
                placeholder="所属项目"
              >
                {option}
              </Select>
            );
          }
          return text;
        },
      },
      {
        title: '计划开始时间',
        dataIndex: 'planTime',
        key: 'planTime',
        width: '12%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <DatePicker
                showTime
                allowClear={false}
                format="YYYY-MM-DD HH:mm:ss"
                defaultValue={moment(text, 'YYYY-MM-DD HH:mm:ss')}
                onChange={e => this.handleFieldChange(e, 'planTime', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="选择计划开始时间"
              />
            );
          }
          return text;
        },
      },
      {
        title: '周期',
        dataIndex: 'cycle',
        key: 'cycle',
        width: '6%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Select
                defaultValue={text}
                value={text}
                onChange={e => this.handleFieldChange(e, 'cycle', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                style={{ width: '100%' }}
                placeholder="周期"
              >
                <Option value="once">一次</Option>
                <Option value="hour">每时</Option>
                <Option value="day">每天</Option>
                <Option value="week">每周</Option>
                <Option value="mouth">每月</Option>
                <Option value="year">每年</Option>
              </Select>
            );
          }
          let cycle = '一次';
          switch (text) {
            case 'once':
              cycle = '一次';
              break;
            case 'hour':
              cycle = '每时';
              break;
            case 'day':
              cycle = '每天';
              break;
            case 'week':
              cycle = '每周';
              break;
            case 'mouth':
              cycle = '每月';
              break;
            case 'year':
              cycle = '每年';
              break;
            default:
              break;
          }
          return cycle;
        },
      },
      {
        title: '状态',
        dataIndex: 'status',
        key: 'status',
        width: '7%',
        filters: [
          { text: '计划中', value: '0' },
          { text: '排队中', value: '1' },
          { text: '测试中', value: '2' },
          { text: '已完成', value: '3' },
          { text: '已暂停', value: '4' },
          { text: '任务异常', value: '5' },
        ],
        render: (text, record) => {
          let status = '计划中';
          switch (text) {
            case 0:
              status = record.url ? (
                <a
                  href={record.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  title="查看最近一次构建日志"
                >
                  计划中
                </a>
              ) : (
                '计划中'
              );
              break;
            case 1:
              status = '排队中';
              break;
            case 2:
              status = record.url ? (
                <a href={record.url} target="_blank" rel="noopener noreferrer" title="查看构建日志">
                  测试中
                </a>
              ) : (
                '测试中'
              );
              break;
            case 3:
              status = record.url ? (
                <a
                  href={record.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  title="查看最近一次构建日志"
                >
                  已完成
                </a>
              ) : (
                '已完成'
              );
              break;
            case 4:
              status = '已暂停';
              break;
            case 5:
              status = '任务异常';
              break;
            default:
              break;
          }
          return status;
        },
      },
      {
        title: '操作',
        key: 'action',
        render: (text, record) => {
          if (!!record.editable && loading) {
            return null;
          }
          if (record.editable) {
            if (record.isNew) {
              return (
                <span>
                  <a onClick={e => this.saveRow(e, record.key)}>添加</a>
                  <Divider type="vertical" />
                  <Popconfirm title="是否要删除此行？" onConfirm={() => this.remove(record)}>
                    <a>删除</a>
                  </Popconfirm>
                </span>
              );
            }
            return (
              <span>
                <a onClick={e => this.saveRow(e, record.key)}>保存</a>
                <Divider type="vertical" />
                <a onClick={e => this.cancel(e, record.key)}>取消</a>
              </span>
            );
          }
          if (currentUser.authority === 'admin' || currentUser.userId === record.userId) {
            return (
              <span>
                <a
                  disabled={record.status === 2}
                  onClick={() => {
                    this.startJob(
                      record.title,
                      record.jid,
                      record.jobName,
                      record.dayBuild,
                      record.runApps,
                      record.email,
                      record.sendMail
                    );
                  }}
                >
                  启动
                </a>
                <Divider type="vertical" />
                <a disabled={record.status === 2} onClick={e => this.toggleEditable(e, record.key)}>
                  编辑
                </a>
                <Divider type="vertical" />
                <Popconfirm
                  title="将会删除该任务相关的测试报告, 是否要删除此行？"
                  onConfirm={() => this.remove(record)}
                >
                  <a disabled={record.status === 2}>删除</a>
                </Popconfirm>
                <Divider type="vertical" />
                <a
                  disabled={record.status === 2}
                  onClick={() => {
                    this.beRunCases(record);
                  }}
                >
                  关联用例
                </a>
              </span>
            );
          }
          return (
            <span>
              <a
                disabled={record.status === 2}
                onClick={() => {
                  this.startJob(
                    record.title,
                    record.jid,
                    record.jobName,
                    record.dayBuild,
                    record.runApps,
                    record.email,
                    record.sendMail
                  );
                }}
              >
                启动
              </a>
              <Divider type="vertical" />
              <a
                disabled={record.status === 2}
                onClick={() => {
                  this.beRunCases(record);
                }}
              >
                关联用例
              </a>
            </span>
          );
        },
      },
    ];
    const {
      removeKeys,
      data,
      visible,
      visibleCases,
      name,
      exec,
      env,
      dayBuild,
      saveOnly,
      sendMail,
      mailList,
      clean,
      selectedCases,
      checkedApps,
      versions,
    } = this.state;
    const hasSelected = removeKeys.length > 0;
    return (
      <Fragment>
        <Row>
          <Col span={20}>
            <Popconfirm
              title="将会删除所选任务相关的测试报告, 是否要删除？"
              onConfirm={() => this.removeRows()}
            >
              <Button type="primary" disabled={!hasSelected}>
                <Icon type="delete" />
                批量删除
              </Button>
            </Popconfirm>
          </Col>
          <Col span={4}>
            <Search
              style={{ marginBottom: 20 }}
              placeholder="按任务编号/名称/描述搜索"
              onSearch={this.onSearchChange}
              enterButton
            />
          </Col>
        </Row>
        <Table
          rowSelection={{
            selections: true,
            onChange: this.onSelectChange,
          }}
          loading={loading || jobsLoading}
          columns={columns}
          dataSource={data}
          pagination={false}
          onChange={this.handleTableChange}
          rowClassName={record => (record.editable ? styles.editable : '')}
          expandedRowRender={record => {
            if (record.editable) {
              return (
                <Fragment>
                  <h3>实际执行时间:</h3>
                  开始时间:&nbsp;&nbsp;
                  {record.startTime}
                  <Divider type="vertical" />
                  结束时间:&nbsp;&nbsp;
                  {record.endTime}
                  <Divider type="vertical" />
                  执行耗时(分钟):&nbsp;&nbsp;
                  {record.time}
                  <Divider />
                  <h3>关联用例:</h3>
                  {record.selectedCases.map(item => (
                    <Tag style={{ marginBottom: 10 }} key={item.key} title={item.title}>
                      {item.cid}
                    </Tag>
                  ))}
                  <Divider />
                  <h3>任务描述:</h3>
                  <TextArea
                    value={record.description}
                    onChange={e => this.handleFieldChange(e, 'description', record.key)}
                    placeholder="任务描述"
                    autosize
                  />
                </Fragment>
              );
            }
            return (
              <Fragment>
                <h3>实际执行时间:</h3>
                开始时间:&nbsp;&nbsp;
                {record.startTime}
                <Divider type="vertical" />
                结束时间:&nbsp;&nbsp;
                {record.endTime}
                <Divider type="vertical" />
                执行耗时(分钟):&nbsp;&nbsp;
                {record.time}
                <Divider />
                <h3>关联用例:</h3>
                {record.selectedCases.map(item => (
                  <Tag style={{ marginBottom: 10 }} key={item.key} title={item.title}>
                    {item.cid}
                  </Tag>
                ))}
                <Divider />
                <h3>任务描述:</h3>
                <TextArea
                  value={record.description}
                  style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
                  placeholder="任务描述"
                  disabled
                  autosize
                />
              </Fragment>
            );
          }}
        />
        <Button
          style={{ width: '100%', marginTop: 16, marginBottom: 8 }}
          type="dashed"
          onClick={this.newMember}
          icon="plus"
        >
          新增任务
        </Button>
        <Row>
          <Col style={{ textAlign: 'right' }}>
            <Pagination
              style={{ marginTop: 16 }}
              showSizeChanger
              showQuickJumper
              hideOnSinglePage
              current={page}
              onChange={this.onPageChange}
              onShowSizeChange={this.onShowSizeChange}
              total={total}
              showTotal={() => '共 '.concat(total.toString()).concat(' 条')}
            />
          </Col>
        </Row>
        <Modal
          title={`启动测试任务(${name})`}
          visible={visible}
          onOk={() => this.handleOk(name)}
          confirmLoading={envLoading || loadingJobs}
          onCancel={this.handleCancel}
          style={{ top: 30 }}
          width="70%"
        >
          <Row style={{ marginBottom: 20 }}>
            <Col span={4} style={{ textAlign: 'right', paddingRight: 20 }}>
              <span>执行器:</span>
            </Col>
            <Col span={20}>
              <Select
                style={{ width: 300 }}
                value={exec}
                placeholder="请选择执行器"
                onSelect={this.selectExec}
              >
                {this.getOption(jenkinsJobs)}
              </Select>
            </Col>
          </Row>
          <Row style={{ marginBottom: 20 }}>
            <Col span={4} style={{ textAlign: 'right', paddingRight: 20 }}>
              <span>测试环境:</span>
            </Col>
            <Col span={20}>
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
            <Col span={4} style={{ textAlign: 'right', paddingRight: 20 }}>
              <span>
                覆盖率监控应用:
                <p style={{ color: 'red' }}>
                  (如需基于版本差异进行覆盖率统计, 请选择差异对比基线版本, 默认选择已登记的最早版本,
                  无版本信息或所选版本与测试环境版本相同则统计全部)
                </p>
              </span>
            </Col>
            <Col span={20}>
              <Checkbox.Group
                onChange={checkedValues => {
                  this.setState({ checkedApps: checkedValues });
                }}
                defaultValue={checkedApps}
                value={checkedApps}
              >
                <Row>
                  {jenkinsApps.map(item => {
                    const version =
                      versions &&
                      Object.keys(versions).includes(item.id) &&
                      versions[item.id].length > 0
                        ? versions
                        : undefined;
                    return (
                      <Col span={8} key={item.key}>
                        <Row style={{ paddingBottom: 10 }}>
                          <Col span={14}>
                            <Checkbox
                              key={item.key}
                              value={item.id}
                              onChange={this.runAppsOnChange}
                            >
                              {item.title}
                            </Checkbox>
                          </Col>
                          <Col span={10}>
                            <Select
                              size="small"
                              style={{ width: 120 }}
                              disabled={!(checkedApps && checkedApps.includes(item.id))}
                              defaultValue={version && version[item.id][0].id}
                              onSelect={this.getVersion}
                            >
                              {version &&
                                versions[item.id].map(ele => (
                                  <Option
                                    key={item.id.concat('_').concat(ele.key)}
                                    title={ele.description}
                                    value={ele.id}
                                  >
                                    {ele.title}
                                  </Option>
                                ))}
                            </Select>
                          </Col>
                        </Row>
                      </Col>
                    );
                  })}
                </Row>
              </Checkbox.Group>
            </Col>
          </Row>
          <Row style={{ marginBottom: 20 }}>
            <Col offset={4} span={20}>
              <Checkbox
                checked={clean}
                onChange={() => {
                  this.setState({ clean: !clean });
                }}
              >
                是否清空上次覆盖率记录?
              </Checkbox>
            </Col>
          </Row>
          <Divider />
          <Row>
            <Col offset={4} span={10}>
              <Row>
                <Col span={18}>
                  <Checkbox
                    checked={dayBuild}
                    onChange={() => {
                      this.setState({ dayBuild: !dayBuild });
                    }}
                  >
                    是否将此环境作为每日构建环境?
                  </Checkbox>
                </Col>
                <Col span={6}>
                  <Checkbox
                    checked={sendMail}
                    onChange={() => {
                      this.setState({ sendMail: !sendMail });
                    }}
                  >
                    发送邮件报告?
                  </Checkbox>
                </Col>
              </Row>
              <Row style={{ marginTop: 20 }}>
                <Col span={10}>
                  <Checkbox
                    checked={saveOnly}
                    onChange={() => {
                      this.setState({ saveOnly: !saveOnly });
                    }}
                  >
                    仅保存配置不启动任务?
                  </Checkbox>
                </Col>
              </Row>
            </Col>
            <Col span={10}>
              <TextArea
                title="一行一个邮箱地址"
                placeholder="请输入邮箱地址, 一行一个"
                style={{ minHeight: 80, maxHeight: 80 }}
                value={mailList.join('\n')}
                onChange={e => {
                  this.setState({ mailList: (e && e.target ? e.target.value : e).split('\n') });
                }}
              />
            </Col>
          </Row>
        </Modal>
        <Modal
          title={`关联测试用例(${name})`}
          visible={visibleCases}
          onOk={this.handleOkCases}
          confirmLoading={caseLoading || loading}
          onCancel={this.handleCancelCases}
          style={{ top: 30 }}
          width="80%"
        >
          <BeRunCasesForm
            testCases={testCases}
            loading={caseLoading}
            onSearch={this.onSearch}
            visible={visibleCases}
            onSelectCases={this.onSelectCases}
            selectedCases={selectedCases}
          />
        </Modal>
      </Fragment>
    );
  }
}

export default JobsForm;
