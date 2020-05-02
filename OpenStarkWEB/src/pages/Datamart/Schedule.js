import React from 'react';
import {
  Divider,
  Input,
  Button,
  Row,
  Col,
  Select,
  Tabs,
  Table,
  Modal,
  Tooltip,
  Popconfirm,
} from 'antd';
import { connect } from 'dva';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';

const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;
const moment = require('moment');

@connect(({ schedule, loading }) => ({
  schedule,
  loading,
}))
class SchedulePage extends React.Component {
  constructor(props) {
    super(props);
    this.onNewClick = this.onNewClick.bind(this);
    this.onEditClick = this.onEditClick.bind(this);
    this.onCopyClick = this.onCopyClick.bind(this);
    this.onDeleteClick = this.onDeleteClick.bind(this);
    this.onCancelClick = this.onCancelClick.bind(this);
    this.onChange = this.onChange.bind(this);
    this.onDataClick = this.onDataClick.bind(this);
    this.onDataChange = this.onDataChange.bind(this);
    this.onCallbackClick = this.onCallbackClick.bind(this);
    this.onCallbackChange = this.onCallbackChange.bind(this);
    this.state = {
      visibleJobNew: false,
      visibleJobsNew: false,
      visibleLog: false,
    };
  }

  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'schedule/getJobs',
    });
    dispatch({
      type: 'schedule/getJob',
    });
  }

  onChange = (cmdType, varName) => e => {
    if (cmdType === 'jobsNew') {
      const { dispatch, schedule } = this.props;
      const { currentJobs } = schedule;
      if (varName === 'interval') {
        dispatch({
          type: 'schedule/save',
          payload: { currentJobs: { ...currentJobs, interval: e.target.value } },
        });
      } else if (varName === 'body') {
        const { data } = currentJobs;
        dispatch({
          type: 'schedule/save',
          payload: {
            currentJobs: {
              ...currentJobs,
              data: {
                ...data,
                body: e.target.value,
              },
            },
          },
        });
      }
    } else if (cmdType === 'jobNew') {
      console.log('varName', varName);
      console.log('e:', e);
      const { dispatch, schedule } = this.props;
      const { current } = schedule;
      if (varName === 'name') {
        dispatch({
          type: 'schedule/save',
          payload: { current: { ...current, name: e.target.value } },
        });
      } else if (varName === 'url') {
        dispatch({
          type: 'schedule/save',
          payload: { current: { ...current, url: e.target.value } },
        });
      } else if (varName === 'method') {
        dispatch({
          type: 'schedule/save',
          payload: { current: { ...current, method: e } },
        });
      } else if (varName === 'cbUrl') {
        const { callback = {} } = current;
        dispatch({
          type: 'schedule/save',
          payload: {
            current: {
              ...current,
              callback: {
                ...callback,
                url: e.target.value,
              },
            },
          },
        });
      } else if (varName === 'cbMethod') {
        const { callback = {} } = current;
        dispatch({
          type: 'schedule/save',
          payload: {
            current: {
              ...current,
              callback: {
                ...callback,
                method: e,
              },
            },
          },
        });
      }
    }
  };

  onDataClick = (cmdType, params = {}) => () => {
    const { schedule, dispatch } = this.props;
    const { currentJobs } = schedule;
    const { data } = currentJobs;
    if (cmdType === 'headersAdd') {
      const { headers } = data;
      const randomNumber = parseInt(Math.random() * 10000, 10);
      headers[`newKey_${randomNumber}`] = '';
      dispatch({
        type: 'schedule/save',
        payload: {
          current: {
            ...currentJobs,
            data: {
              ...data,
              headers,
            },
          },
        },
      });
    } else if (cmdType === 'paramsAdd') {
      const { params: paramsSave } = data;
      const randomNumber = parseInt(Math.random() * 10000, 10);
      paramsSave[`newKey_${randomNumber}`] = '';
      dispatch({
        type: 'schedule/save',
        payload: {
          current: {
            ...currentJobs,
            data: {
              ...data,
              params: paramsSave,
            },
          },
        },
      });
    } else if (cmdType === 'queryAdd') {
      const { query } = data;
      const randomNumber = parseInt(Math.random() * 10000, 10);
      query[`newKey_${randomNumber}`] = '';
      dispatch({
        type: 'schedule/save',
        payload: {
          current: {
            ...currentJobs,
            data: {
              ...data,
              query,
            },
          },
        },
      });
    } else if (cmdType === 'headersDelete') {
      const { headers } = data;
      const { key } = params;
      delete headers[key];
      dispatch({
        type: 'schedule/save',
        payload: {
          current: {
            ...currentJobs,
            data: {
              ...data,
              headers,
            },
          },
        },
      });
    } else if (cmdType === 'paramsDelete') {
      const { params: paramsSave } = data;
      const { key } = params;
      delete paramsSave[key];
      dispatch({
        type: 'schedule/save',
        payload: {
          current: {
            ...currentJobs,
            data: {
              ...data,
              params: paramsSave,
            },
          },
        },
      });
    } else if (cmdType === 'queryDelete') {
      const { query } = data;
      const { key } = params;
      delete query[key];
      dispatch({
        type: 'schedule/save',
        payload: {
          current: {
            ...currentJobs,
            data: {
              ...data,
              query,
            },
          },
        },
      });
    }
  };

  onDataChange = (cmdType, key) => e => {
    if (cmdType === 'keyHeaders') {
      const { schedule, dispatch } = this.props;
      const { currentJobs } = schedule;
      const { data = {} } = currentJobs;
      const { headers = {} } = data;
      if (key !== e.target.value) {
        headers[e.target.value] = headers[key];
        delete headers[key];
      }

      dispatch({
        type: 'schedule/save',
        payload: {
          currentJobs: {
            ...currentJobs,
            data: {
              ...data,
              headers,
            },
          },
        },
      });
    } else if (cmdType === 'keyParams') {
      const { schedule, dispatch } = this.props;
      const { currentJobs } = schedule;
      const { data = {} } = currentJobs;
      const { params = {} } = data;
      if (key !== e.target.value) {
        params[e.target.value] = params[key];
        delete params[key];
      }

      dispatch({
        type: 'schedule/save',
        payload: {
          currentJobs: {
            ...currentJobs,
            data: {
              ...data,
              params,
            },
          },
        },
      });
    } else if (cmdType === 'keyQuery') {
      const { schedule, dispatch } = this.props;
      const { currentJobs } = schedule;
      const { data = {} } = currentJobs;
      const { query = {} } = data;
      if (key !== e.target.value) {
        query[e.target.value] = query[key];
        delete query[key];
      }

      dispatch({
        type: 'schedule/save',
        payload: {
          currentJobs: {
            ...currentJobs,
            data: {
              ...data,
              query,
            },
          },
        },
      });
    } else if (cmdType === 'valueHeaders') {
      const { schedule, dispatch } = this.props;
      const { currentJobs } = schedule;
      const { data = {} } = currentJobs;
      const { headers = {} } = data;
      const newHeaders = headers;
      newHeaders[key] = e.target.value;
      dispatch({
        type: 'schedule/save',
        payload: {
          currentJobs: {
            ...currentJobs,
            data: {
              ...data,
              headers: newHeaders,
            },
          },
        },
      });
    } else if (cmdType === 'valueParams') {
      const { schedule, dispatch } = this.props;
      const { currentJobs } = schedule;
      const { data = {} } = currentJobs;
      const { params = {} } = data;
      const newParams = params;
      newParams[key] = e.target.value;
      dispatch({
        type: 'schedule/save',
        payload: {
          currentJobs: {
            ...currentJobs,
            data: {
              ...data,
              params: newParams,
            },
          },
        },
      });
    } else if (cmdType === 'valueQuery') {
      const { schedule, dispatch } = this.props;
      const { currentJobs } = schedule;
      const { data = {} } = currentJobs;
      const { query = {} } = data;
      const newQuery = query;
      newQuery[key] = e.target.value;
      dispatch({
        type: 'schedule/save',
        payload: {
          currentJobs: {
            ...currentJobs,
            data: {
              ...data,
              query: newQuery,
            },
          },
        },
      });
    }
  };

  onCallbackClick = (cmdType, params = {}) => () => {
    if (cmdType === 'newAdd') {
      const { schedule, dispatch } = this.props;
      const { current } = schedule;
      const { callback = {} } = current;
      const { headers = {} } = callback;
      const randomNumber = parseInt(Math.random() * 10000, 10);
      headers[`newKey_${randomNumber}`] = '';
      dispatch({
        type: 'schedule/save',
        payload: {
          current: {
            ...current,
            callback: {
              ...callback,
              headers,
            },
          },
        },
      });
    } else if (cmdType === 'newDelete') {
      const { key } = params;
      const { schedule, dispatch } = this.props;
      const { current } = schedule;
      const { callback = {} } = current;
      const { headers = {} } = callback;
      delete headers[key];
      dispatch({
        type: 'schedule/save',
        payload: {
          current: {
            ...current,
            callback: {
              ...callback,
              headers,
            },
          },
        },
      });
    }
  };

  onCallbackChange = (cmdType, key) => e => {
    if (cmdType === 'key') {
      const { schedule, dispatch } = this.props;
      const { current } = schedule;
      const { callback = {} } = current;
      const { headers = {} } = callback;
      if (key !== e.target.value) {
        headers[e.target.value] = headers[key];
        delete headers[key];
      }

      dispatch({
        type: 'schedule/save',
        payload: {
          current: {
            ...current,
            callback: {
              ...callback,
              headers,
            },
          },
        },
      });
    } else if (cmdType === 'value') {
      const { schedule, dispatch } = this.props;
      const { current } = schedule;
      const { callback = {} } = current;
      const { headers = {} } = callback;
      const newHeaders = headers;
      newHeaders[key] = e.target.value;
      dispatch({
        type: 'schedule/save',
        payload: {
          current: {
            ...current,
            callback: {
              ...callback,
              headers: newHeaders,
            },
          },
        },
      });
    }
  };

  onCancelClick = name => () => {
    const { dispatch, schedule } = this.props;
    const { currentJobs } = schedule;

    dispatch({
      type: 'schedule/save',
      payload: {
        currentJobs: {
          ...currentJobs,
          name,
        },
      },
    });
    dispatch({ type: 'schedule/runCancel' });
  };

  onNewClick = (cmdType, name) => () => {
    if (cmdType === 'job') {
      // 隐藏窗口
      this.setState({ visibleJobNew: false });
      const { dispatch } = this.props;
      dispatch({
        type: 'schedule/newJob',
      });
    } else if (cmdType === 'jobs') {
      // 隐藏窗口
      this.setState({ visibleJobsNew: false });
      const { dispatch } = this.props;
      dispatch({
        type: 'schedule/newJobs',
      });
    } else if (cmdType === 'addJob') {
      const { dispatch } = this.props;
      dispatch({
        type: 'schedule/save',
        payload: { op: 2 },
      });
      this.setState({ visibleJobNew: true });
    } else if (cmdType === 'addJobs0') {
      const { dispatch, schedule } = this.props;
      const { currentJobs } = schedule;
      dispatch({
        type: 'schedule/save',
        payload: {
          runMode: 0,
          currentJobs: {
            ...currentJobs,
            name,
          },
        },
      });
      this.setState({ visibleJobsNew: true });
    } else if (cmdType === 'addJobs1') {
      const { dispatch, schedule } = this.props;
      const { currentJobs } = schedule;
      dispatch({
        type: 'schedule/save',
        payload: {
          runMode: 1,
          currentJobs: {
            ...currentJobs,
            name,
          },
        },
      });
      this.setState({ visibleJobsNew: true });
    } else if (cmdType === 'addJobs2') {
      const { dispatch, schedule } = this.props;
      const { currentJobs } = schedule;
      dispatch({
        type: 'schedule/save',
        payload: {
          runMode: 2,
          currentJobs: {
            ...currentJobs,
            name,
          },
        },
      });
      this.setState({ visibleJobsNew: true });
    } else {
      console.log('cmdType:', cmdType);
    }
  };

  onUpdateClick = cmdType => () => {
    if (cmdType === 'job') {
      // 隐藏窗口
      this.setState({ visibleJobNew: false });
      const { dispatch } = this.props;
      dispatch({
        type: 'schedule/updateJob',
      });
    } else {
      console.log('cmdType:', cmdType);
    }
  };

  onEditClick = (cmdType, name) => () => {
    if (cmdType === 'job') {
      const { dispatch } = this.props;
      dispatch({
        type: 'schedule/copyJob',
        payload: { name, op: 1 },
      }).then(() => {
        this.setState({ visibleJobNew: true });
      });
    } else {
      console.log('cmdType:', cmdType);
    }
  };

  onCopyClick = (cmdType, name) => () => {
    if (cmdType === 'job') {
      const { dispatch } = this.props;
      dispatch({
        type: 'schedule/copyJob',
        payload: { name, op: 0 },
      }).then(() => {
        this.setState({ visibleJobNew: true });
      });
    } else {
      console.log('cmdType:', cmdType);
    }
  };

  onDeleteClick = (cmdType, name) => () => {
    if (cmdType === 'job') {
      const { dispatch } = this.props;
      dispatch({
        type: 'schedule/deleteJob',
        payload: { name },
      });
    } else {
      console.log('cmdType:', cmdType);
    }
  };

  getAgendas() {
    const renderItem = [];
    const { schedule } = this.props;
    const { jobs } = schedule;
    if (!jobs) {
      return renderItem;
    }
    const list = jobs.jobs;
    const columns = [
      {
        title: 'Status',
        dataIndex: 'name',
        key: 'name',
        render: (text, record) => (
          <Button.Group>
            {record.repeating ? (
              <Button htmlType="button" type="primary" ghost>
                {record.job.repeatInterval}
              </Button>
            ) : (
              ''
            )}
            {record.scheduled ? (
              <Button htmlType="button" type="primary" ghost>
                scheduled
              </Button>
            ) : (
              ''
            )}
            {record.queued ? (
              <Button htmlType="button" type="primary" ghost>
                queued
              </Button>
            ) : (
              ''
            )}
            {record.running ? (
              <Button htmlType="button" type="primary" ghost>
                running
              </Button>
            ) : (
              ''
            )}
            {record.completed ? (
              <Button htmlType="button" type="primary" ghost>
                completed
              </Button>
            ) : (
              ''
            )}
            {record.failed ? (
              <Button htmlType="button" type="danger" ghost>
                failed
              </Button>
            ) : (
              ''
            )}
          </Button.Group>
        ),
      },
      {
        title: 'Name',
        dataIndex: 'job.name',
        key: 'job.name',
      },
      {
        title: 'Last run started',
        dataIndex: 'job.lastRunAt',
        key: 'job.lastRunAt',
        render: text => {
          const t = text ? moment(text).fromNow() : '';
          return <div>{t}</div>;
        },
      },
      {
        title: 'Next run starts',
        dataIndex: 'job.nextRunAt',
        key: 'job.nextRunAt',
        render: text => {
          const t = text ? moment(text).fromNow() : '';
          return <div>{t}</div>;
        },
      },
      {
        title: 'Last finished',
        dataIndex: 'job.lastFinishedAt',
        key: 'job.lastFinishedAt',
        render: text => {
          const t = text ? moment(text).fromNow() : '';
          return <div>{t}</div>;
        },
      },
      {
        title: 'Locked',
        dataIndex: 'job.lockedAt',
        key: 'job.lockedAt',
        render: text => {
          const t = text ? moment(text).fromNow() : '';
          return <div>{t}</div>;
        },
      },
      {
        title: '日志',
        dataIndex: 'failReason',
        key: 'failReason',
        render: (text, record) => {
          const logContent = (
            <TextArea value={JSON.stringify(record, null, 2)} style={{ width: 800, height: 600 }} />
          );

          return <Popconfirm title={logContent}> 查看 </Popconfirm>;
        },
      },
    ];
    if (list) {
      renderItem.push(<Divider key="DividerJob0">-</Divider>);
      renderItem.push(
        <Table
          rowKey="_id"
          key="TableJob0"
          dataSource={list}
          columns={columns}
          pagination={{
            total: list.count,
            position: 'bottom',
            size: 'small',
            pageSize: 5,
            defaultPageSize: 5,
            pageSizeOptions: ['5', '10', '20', '50', '100'],
            showQuickJumper: true,
            hideOnSinglePage: false,
            showSizeChanger: true,
            showTotal: total => `共 ${total} 条`,
          }}
        />
      );
    }

    return renderItem;
  }

  getJobLayout() {
    const renderItem = [];
    const { schedule } = this.props;
    const { list } = schedule;
    const columns = [
      {
        title: '任务名称',
        dataIndex: 'name',
        key: 'name',
      },
      {
        title: '功能实现Url',
        dataIndex: 'url',
        key: 'age',
      },
      {
        title: 'HTTP方法',
        dataIndex: 'method',
        key: 'method',
        render: text => <div>{text || 'POST'}</div>,
      },
      {
        title: '回调',
        dataIndex: 'callback',
        key: 'callback',
        render: text => <div>{JSON.stringify(text, 4) || '空'}</div>,
      },
      {
        title: '操作',
        dataIndex: '_id',
        key: '_id',
        render: (text, record) => {
          const { name } = record;
          return (
            <div>
              <Button.Group>
                <Button
                  htmlType="button"
                  type="primary"
                  size="small"
                  onClick={this.onEditClick('job', name)}
                >
                  编辑
                </Button>
                <Button
                  htmlType="button"
                  type="second"
                  size="small"
                  onClick={this.onCopyClick('job', name)}
                >
                  复制
                </Button>
                <Button htmlType="button" size="small" onClick={this.onDeleteClick('job', name)}>
                  删除
                </Button>
              </Button.Group>
              &nbsp;&nbsp;&nbsp;&nbsp;
              <Button.Group>
                <Button
                  htmlType="button"
                  type="primary"
                  size="small"
                  onClick={this.onNewClick('addJobs0', name)}
                >
                  周期调度
                </Button>
                <Button htmlType="button" size="small" onClick={this.onNewClick('addJobs1', name)}>
                  单次调度
                </Button>
                <Button htmlType="button" size="small" onClick={this.onNewClick('addJobs2', name)}>
                  立即调度
                </Button>
              </Button.Group>
              &nbsp;&nbsp;&nbsp;&nbsp;
              <Button.Group>
                <Button
                  htmlType="button"
                  type="fail"
                  size="small"
                  onClick={this.onCancelClick(name)}
                >
                  取消调度
                </Button>
              </Button.Group>
            </div>
          );
        },
      },
    ];
    if (list) {
      renderItem.push(<Divider key="DividerJob0">-</Divider>);
      renderItem.push(
        <Table
          rowKey="_id"
          key="TableJob0"
          dataSource={list}
          columns={columns}
          title={() => (
            <Button.Group>
              <Button type="primary" onClick={this.onNewClick('addJob')}>
                新建Job
              </Button>
            </Button.Group>
          )}
          pagination={{
            total: list.count,
            position: 'bottom',
            size: 'small',
            pageSize: 5,
            defaultPageSize: 5,
            pageSizeOptions: ['5', '10', '20', '50', '100'],
            showQuickJumper: true,
            hideOnSinglePage: false,
            showSizeChanger: true,
            showTotal: total => `共 ${total} 条`,
          }}
        />
      );
    }

    return renderItem;
  }

  getModalsJobs() {
    const renderItem = [];
    const { visibleJobsNew } = this.state;
    const { schedule } = this.props;
    const { currentJobs, runMode } = schedule;
    const { name = 'default', interval = '', data } = currentJobs;
    const { headers, params, query, body = '' } = data;
    let headersItem = [];
    let paramsItem = [];
    let queryItem = [];

    if (headers) {
      headersItem = Object.keys(headers).map((key, index) => {
        const keyInput = (
          <Input
            defaultValue={key}
            addonBefore={index + 1}
            style={{ width: 200 }}
            onPressEnter={this.onDataChange('keyHeadrs', key)}
            onBlur={this.onDataChange('keyHeaders', key)}
          />
        );
        const op = (
          <Button htmlType="button" onClick={this.onDataClick('headersDelete', { key, index })}>
            -
          </Button>
        );
        return (
          <Row key={key}>
            <Col>
              <Input
                addonBefore={keyInput}
                value={headers[key]}
                addonAfter={op}
                onChange={this.onDataChange('valueHeaders', key)}
              />
            </Col>
          </Row>
        );
      });
    }

    if (params) {
      paramsItem = Object.keys(params).map((key, index) => {
        const keyInput = (
          <Input
            defaultValue={key}
            addonBefore={index + 1}
            style={{ width: 200 }}
            onPressEnter={this.onDataChange('keyParams', key)}
            onBlur={this.onDataChange('keyParams', key)}
          />
        );
        const op = (
          <Button htmlType="button" onClick={this.onDataClick('paramsDelete', { key, index })}>
            -
          </Button>
        );
        return (
          <Row key={key}>
            <Col>
              <Input
                addonBefore={keyInput}
                value={params[key]}
                addonAfter={op}
                onChange={this.onDataChange('valueParams', key)}
              />
            </Col>
          </Row>
        );
      });
    }

    if (query) {
      queryItem = Object.keys(query).map((key, index) => {
        const keyInput = (
          <Input
            defaultValue={key}
            addonBefore={index + 1}
            style={{ width: 200 }}
            onPressEnter={this.onDataChange('keyQuery', key)}
            onBlur={this.onDataChange('keyQuery', key)}
          />
        );
        const op = (
          <Button htmlType="button" onClick={this.onDataClick('queryDelete', { key, index })}>
            -
          </Button>
        );
        return (
          <Row key={key}>
            <Col>
              <Input
                addonBefore={keyInput}
                value={query[key]}
                addonAfter={op}
                onChange={this.onDataChange('valueQuery', key)}
              />
            </Col>
          </Row>
        );
      });
    }
    let title = '周期调度';
    if (runMode === 0) {
      title = '周期调度';
    } else if (runMode === 1) {
      title = '单次调度';
    } else if (runMode === 2) {
      title = '立即调度';
    }
    renderItem.push(
      <Modal
        key="jobNew"
        title={title}
        visible={visibleJobsNew}
        okText="保存"
        onOk={this.onNewClick('jobs')}
        cancelText="放弃"
        onCancel={() => this.setState({ visibleJobsNew: false })}
      >
        <Divider>基本参数</Divider>
        <Row>
          <Col>
            *<b>任务名称</b>
          </Col>
          <Col>
            <Input value={name} onChange={this.onChange('jobsNew', 'name')} />
          </Col>
        </Row>
        <Row>
          <Col>
            *<b>interval</b>
          </Col>
          <Col>
            <Input value={interval} onChange={this.onChange('jobsNew', 'interval')} />
          </Col>
        </Row>
        <Divider>data(可选)</Divider>
        <Row>
          <Col>
            <b>headers</b>
            <Button htmlType="button" onClick={this.onDataClick('headersAdd')}>
              +
            </Button>
          </Col>
          <Col>{headersItem}</Col>
        </Row>
        <Row>
          <Col>
            <b>params</b>
            <Button htmlType="button" onClick={this.onDataClick('paramsAdd')}>
              +
            </Button>
          </Col>
          <Col>{paramsItem}</Col>
        </Row>
        <Row>
          <Col>
            <b>query</b>
            <Button htmlType="button" onClick={this.onDataClick('queryAdd')}>
              +
            </Button>
          </Col>
          <Col>{queryItem}</Col>
        </Row>
        <Row>
          <Col>
            *<b>body</b>
          </Col>
          <Col>
            <Input value={body} onChange={this.onChange('jobsNew', 'body')} />
          </Col>
        </Row>
      </Modal>
    );
    return renderItem;
  }

  getModalsJob() {
    const renderItem = [];
    const { visibleJobNew } = this.state;
    const { current, op = 0 } = this.props.schedule;
    const { name = 'default', url = '', method = 'POST', callback = {} } = current;

    const { url: cbUrl = '', method: cbMethod = 'POST', headers = {} } = callback;
    const urlPre = (
      <Select defaultValue="POST" onChange={this.onChange('jobNew', 'method')}>
        <Option value="POST">POST</Option>
        <Option value="GET">GET</Option>
        <Option value="DELETE">DELETE</Option>
        <Option value="PUT">PUT</Option>
      </Select>
    );
    const cbUrlPre = (
      <Select defaultValue="POST" onChange={this.onChange('jobNew', 'cbMethod')}>
        <Option value="POST">POST</Option>
        <Option value="GET">GET</Option>
        <Option value="DELETE">DELETE</Option>
        <Option value="PUT">PUT</Option>
      </Select>
    );

    const headersItem = Object.keys(headers).map((key, index) => {
      const keyInput = (
        <Input
          defaultValue={key}
          addonBefore={index + 1}
          style={{ width: 200 }}
          onPressEnter={this.onCallbackChange('key', key)}
          onBlur={this.onCallbackChange('key', key)}
        />
      );
      const op = (
        <Button htmlType="button" onClick={this.onCallbackClick('newDelete', { key, index })}>
          -
        </Button>
      );
      return (
        <Row key={key}>
          <Col>
            <Input
              addonBefore={keyInput}
              value={headers[key]}
              addonAfter={op}
              onChange={this.onCallbackChange('value', key)}
            />
          </Col>
        </Row>
      );
    });

    renderItem.push(
      <Modal
        key="jobNew"
        title={op === 0 || op === 2 ? '新建Job' : '编辑Job'}
        visible={visibleJobNew}
        okText="保存"
        onOk={op === 0 || op === 2 ? this.onNewClick('job') : this.onUpdateClick('job')}
        cancelText="放弃"
        onCancel={() => this.setState({ visibleJobNew: false })}
      >
        <Divider>基本参数</Divider>
        <Row>
          <Col>
            *<b>任务名称</b>
          </Col>
          <Col>
            <Input value={name} onChange={this.onChange('jobNew', 'name')} disabled={op === 1} />
          </Col>
        </Row>
        <Row>
          <Col>
            *<b>url</b>
          </Col>
          <Col>
            <Input addonBefore={urlPre} value={url} onChange={this.onChange('jobNew', 'url')} />
          </Col>
        </Row>
        <Divider>回调参数(可选)</Divider>
        <Row>
          <Col>
            *<b>url</b>
          </Col>
          <Col>
            <Input
              addonBefore={cbUrlPre}
              value={cbUrl || ''}
              onChange={this.onChange('jobNew', 'cbUrl')}
            />
          </Col>
        </Row>
        <Row>
          <Col>
            <b>headers</b>
            <Button htmlType="button" onClick={this.onCallbackClick('newAdd')}>
              +
            </Button>
          </Col>
          <Col>{headersItem}</Col>
        </Row>
      </Modal>
    );
    return renderItem;
  }

  render() {
    const agendas = this.getAgendas();
    const job = this.getJobLayout();
    const modalsJob = this.getModalsJob();
    const modalsJobs = this.getModalsJobs();

    return (
      <PageHeaderWrapper>
        <Tabs key="inputTab" tabPosition="top" defaultActiveKey="agenda">
          <TabPane tab="调度管理" key="agenda">
            {agendas}
          </TabPane>
          <TabPane tab="任务维护" key="job">
            {job}
          </TabPane>
        </Tabs>
        {modalsJob} {modalsJobs}
      </PageHeaderWrapper>
    );
  }
}

export default SchedulePage;
