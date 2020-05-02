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
} from 'antd';
import moment from 'moment';
import { connect } from 'dva';
import styles from '../Tools/style.less';

const { TextArea, Search } = Input;
const { Option } = Select;

@connect(({ environment, jobs, guiTest, loading }) => ({
  server: environment.envList.data || [],
  jenkinsJobs: jobs.jenkinsJobs,
  jenkinsApps: jobs.jenkinsApps,
  testCases: guiTest.testCases,
  envLoading: loading.effects['environment/fetchEnv'],
  loadingJobs: loading.effects['jobs/getJenkins'],
  caseLoading: loading.effects['guiTest/fetchGuiTest'],
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
      versions: {},
      selectedVersions: {},
      env: [],
      jobId: undefined,
      saveOnly: false,
      clean: false,
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

  getRowByKey(key, newData) {
    const { data } = this.state;
    return (newData || data).filter(item => item.key === key)[0];
  }

  startJob = (name, jobId, dayBuild, runApps) => {
    const { dispatch } = this.props;
    dispatch({
      type: 'environment/fetchEnv',
      op: 'server',
      action: 'all',
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
      env: Array.isArray(dayBuild) ? dayBuild : [],
      checkedApps: runApps,
    });
  };

  stopJob = (jobId, name) => {
    const { dispatch } = this.props;
    const { filters } = this.state;
    dispatch({
      type: 'jobs/runJenkins',
      op: 'stopJob',
      payload: {
        jobId,
        name,
      },
      callback: () => {
        this.onSearchChange(filters);
      },
    });
  };

  handleOk = name => {
    const { dispatch } = this.props;
    const { env, jobId, filters, saveOnly, checkedApps, clean, selectedVersions } = this.state;
    if (env.length > 0) {
      Object.keys(selectedVersions).forEach(item => {
        if (!checkedApps.includes(item)) {
          delete selectedVersions[item];
        }
      });
      dispatch({
        type: 'jobs/runJenkins',
        op: 'jobs',
        payload: {
          env,
          name,
          jobId,
          type: 'test',
          saveOnly,
          clean,
          runApps: checkedApps,
          checkVersion: selectedVersions,
        },
        callback: () => {
          this.onSearchChange(filters);
        },
      });
      this.setState({
        visible: false,
      });
    } else {
      message.error('请选择测试环境!');
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

  selectServer = item => {
    const { env } = this.state;
    env.push(item);
    this.setState({ env: env.map(ele => ele) });
  };

  onDeselectServer = item => {
    const { env } = this.state;
    let newenv = [];
    newenv = env.filter(ele => ele !== item);
    this.setState({ env: newenv });
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
      planTime: new Date(),
      startTime: '',
      endTime: '',
      time: '',
      userId: currentUser.userId,
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

  getVersion = (value, e) => {
    const { selectedVersions } = this.state;
    selectedVersions[e.key.split('_')[0]] = value;
    this.setState({ selectedVersions });
  };

  remove(record) {
    const { data, filters, removeKeys } = this.state;
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

  saveRow(e, key) {
    const { editRows } = this.props;
    e.persist();
    if (this.clickedCancel) {
      this.clickedCancel = false;
      return;
    }
    const target = this.getRowByKey(key) || {};
    if (!target.pid || !target.title || !target.planTime) {
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
      jobsLoading,
      server,
      jenkinsApps,
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
        width: '15%',
        render: text => text,
      },
      {
        title: '任务名称',
        dataIndex: 'title',
        key: 'title',
        width: '15%',
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
        title: '状态',
        dataIndex: 'status',
        key: 'status',
        width: '8%',
        filters: [
          { text: '计划中', value: '0' },
          { text: '测试中', value: '2' },
          { text: '已完成', value: '3' },
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
                    this.startJob(record.title, record.jid, record.dayBuild, record.runApps);
                  }}
                >
                  启动
                </a>
                <Divider type="vertical" />
                <Popconfirm
                  title="确定要停止任务？"
                  onConfirm={() => {
                    this.stopJob(record.jid, record.title);
                  }}
                >
                  <a disabled={record.status !== 2}>停止</a>
                </Popconfirm>
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
              </span>
            );
          }
          return (
            <span>
              <a
                disabled={record.status === 2}
                onClick={() => {
                  this.startJob(record.title, record.jid, record.dayBuild, record.runApps);
                }}
              >
                启动
              </a>
              <Divider type="vertical" />
              <Popconfirm
                title="确定要停止任务？"
                onConfirm={() => {
                  this.stopJob(record.jid, record.title);
                }}
              >
                <a disabled={record.status !== 2}>停止</a>
              </Popconfirm>
            </span>
          );
        },
      },
    ];
    const {
      removeKeys,
      data,
      visible,
      name,
      env,
      saveOnly,
      clean,
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
          style={{ top: 50 }}
          width="70%"
        >
          <Row style={{ marginBottom: 20 }}>
            <Col span={4} style={{ textAlign: 'right', paddingRight: 20 }}>
              <span>测试环境:</span>
            </Col>
            <Col span={20}>
              <Select
                style={{ width: 300 }}
                value={env}
                mode="multiple"
                placeholder="请选择测试环境"
                onSelect={this.selectServer}
                onDeselect={this.onDeselectServer}
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
                                version[item.id].map(ele => (
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
            <Col offset={4} span={20}>
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
        </Modal>
      </Fragment>
    );
  }
}

export default JobsForm;
