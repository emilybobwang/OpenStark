import React, { PureComponent, Fragment } from 'react';
import { connect } from 'dva';
import { Table, Input, Divider, Row, Col, Popconfirm, Button, Icon } from 'antd';
import Link from 'umi/link';

const { TextArea, Search } = Input;

@connect(({ user, jobs, project, loading }) => ({
  reports: jobs.reports,
  editResult: jobs.runResult,
  currentUser: user.currentUser,
  project,
  loading: loading.effects['jobs/fetchReports'],
  editLoading: loading.effects['jobs/runJenkins'],
}))
class JacocoReportsForm extends PureComponent {
  constructor(props) {
    super(props);

    this.state = {
      data: [],
      filters: {
        keyWord: '',
      },
      removeKeys: [],
    };
  }

  componentDidMount() {
    const {
      dispatch,
      match: { url },
    } = this.props;
    dispatch({
      type: 'jobs/fetchReports',
      op: 'jacoco',
      payload: {
        type: url.split('/')[1],
      },
    });
    dispatch({
      type: 'project/fetchProjects',
      payload: {
        type: 'projects',
      },
    });
    dispatch({
      type: 'project/fetchTeams',
      payload: {
        type: 'teams',
      },
    });
  }

  componentWillReceiveProps(nextProps) {
    if ('reports' in nextProps) {
      const {
        reports: { data },
      } = nextProps;
      this.setState({
        data,
      });
    }
  }

  onSearch = filters => {
    const {
      reports,
      dispatch,
      match: { url },
    } = this.props;
    dispatch({
      type: 'jobs/fetchReports',
      payload: {
        size: reports.size,
        ...filters,
        type: url.split('/')[1],
      },
      op: 'jacoco',
    });
  };

  editRows = data => {
    const {
      match: { url },
      dispatch,
    } = this.props;
    dispatch({
      type: 'jobs/runJenkins',
      payload: {
        ...data,
        type: url.split('/')[1],
        action: 'delete',
      },
      op: 'jacoco',
      callback: ()=>{
        const { filters } = this.state;
        this.onSearchChange(filters);
      },
    });
  };

  refreshRows = data => {
    const {
      match: { url },
      dispatch,
    } = this.props;
    dispatch({
      type: 'jobs/runJenkins',
      payload: {
        ...data,
        type: url.split('/')[1],
        action: 'refresh',
      },
      op: 'jacoco',
      callback:()=>{
        const { filters } = this.state;
        this.onSearchChange(filters);
      },
    });
  };

  onSearchChange = filter => {
    const { filters } = this.state;
    const keyWords = filters;
    if (typeof filter === 'string') {
      keyWords.keyWord = filter;
    }
    this.onSearch(keyWords);
    this.setState({
      filters: keyWords,
    });
  };

  handleTableChange = (pagination, filter) => {
    const { filters } = this.state;
    const search = filters;
    if (Object.keys(filter).includes('pid')) {
      search.pid = filter.pid.join(',');
    }
    if (Object.keys(filter).includes('tid')) {
      search.tid = filter.tid.join(',');
    }
    search.page = pagination.current;
    search.size = pagination.pageSize;
    this.onSearchChange(search);
  };

  removeRows = () => {
    const { data, removeKeys } = this.state;
    const newData = data.filter(item => removeKeys.indexOf(item.key) === -1);
    const rowKeys = removeKeys.filter(item => typeof item === 'number');
    this.setState({ data: newData });
    if (rowKeys.length > 0) {
      this.editRows({ key: rowKeys });
    }
    this.setState({
      removeKeys: [],
    });
  };

  onSelectChange = (selectedRowKeys, selectedRows) => {
    const { currentUser } = this.props;
    const { removeKeys } = this.state;
    const selected = selectedRows
      .filter(element => currentUser.authority === 'admin' || element.userId === currentUser.userId)
      .map(item => item.key);
    const removeKeysList = selectedRowKeys.filter(
      item => removeKeys.indexOf(item) >= 0 || selected.indexOf(item) >= 0
    );
    this.setState({
      removeKeys: removeKeysList,
    });
  };

  remove(record) {
    const { data } = this.state;
    const newData = data.filter(item => item.key !== record.key);
    this.setState({ data: newData });
    this.editRows(record);
  }

  render() {
    const {
      loading,
      editLoading,
      reports: { total, page },
      project: { projectsList, teams },
      currentUser,
      match: { url },
    } = this.props;
    const columns = [
      {
        title: '#',
        dataIndex: 'no',
        key: 'no',
        width: '4%',
        render: text => text,
      },
      {
        title: '报告日期',
        dataIndex: 'date',
        key: 'date',
        width: '8%',
        render: text => text,
      },
      {
        title: '任务名称',
        dataIndex: 'title',
        key: 'title',
        width: '12%',
        render: text => text,
      },
      {
        title: '所属组',
        dataIndex: 'team',
        key: 'tid',
        filters: teams.map(item => ({ text: item.name, value: item.tid })),
        width: '12%',
        render: text => text,
      },
      {
        title: '所属项目',
        dataIndex: 'project',
        key: 'pid',
        filters: projectsList.map(item => ({ text: item.name, value: item.pid })),
        width: '12%',
        render: text => text,
      },
      {
        title: 'LINE',
        dataIndex: 'line',
        key: 'line',
        width: '8%',
        render: text =>
          (text * 100)
            .toFixed(2)
            .toString()
            .concat(' %'),
      },
      {
        title: 'BRANCH',
        dataIndex: 'branch',
        key: 'branch',
        width: '8%',
        render: text =>
          (text * 100)
            .toFixed(2)
            .toString()
            .concat(' %'),
      },
      {
        title: 'METHOD',
        dataIndex: 'method',
        key: 'method',
        width: '8%',
        render: text =>
          (text * 100)
            .toFixed(2)
            .toString()
            .concat(' %'),
      },
      {
        title: 'CLASS',
        dataIndex: 'classes',
        key: 'classes',
        width: '8%',
        render: text =>
          (text * 100)
            .toFixed(2)
            .toString()
            .concat(' %'),
      },
      {
        title: '操作',
        key: 'action',
        render: (text, record) => {
          if (currentUser.authority === 'admin' || currentUser.userId === record.userId) {
            return (
              <span>
                <Link to={`/${url.split('/')[1]}/reports/jacoco/${record.jid}/${record.date}`}>
                  详情
                </Link>
                <Divider type="vertical" />
                <a
                  onClick={() => {
                    this.refreshRows(record);
                  }}
                >
                  刷新
                </a>
                <Divider type="vertical" />
                <Popconfirm title="确定删除该JaCoCo报告？" onConfirm={() => this.remove(record)}>
                  <a>删除</a>
                </Popconfirm>
              </span>
            );
          }
          return (
            <span>
              <Link to={`/${url.split('/')[1]}/reports/jacoco/${record.jid}/${record.date}`}>
                详情
              </Link>
              <Divider type="vertical" />
              <a
                onClick={() => {
                  this.refreshRows(record);
                }}
              >
                刷新
              </a>
            </span>
          );
        },
      },
    ];
    const { removeKeys, data } = this.state;
    const hasSelected = removeKeys.length > 0;
    return (
      <Fragment>
        <Row>
          <Col span={20}>
            <Popconfirm
              title="将会删除所选任务相关的JaCoCo报告, 是否要删除？"
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
          loading={loading || editLoading}
          columns={columns}
          dataSource={data}
          pagination={{
            showSizeChanger: true,
            showQuickJumper: true,
            hideOnSinglePage: true,
            current: page,
            total,
            showTotal: () => '共 '.concat(total).concat(' 条'),
          }}
          onChange={this.handleTableChange}
          expandedRowRender={record => {
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
                {record.runTime}
                <Divider />
                <h3>报告描述:</h3>
                <TextArea
                  value={record.description}
                  style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
                  placeholder="报告描述"
                  disabled
                  autosize
                />
              </Fragment>
            );
          }}
        />
      </Fragment>
    );
  }
}

export default JacocoReportsForm;
