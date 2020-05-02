import React, { PureComponent, Fragment } from 'react';
import { Table, Input, message, Divider, Row, Col, Popconfirm, Button, Icon } from 'antd';
import Link from 'umi/link';
import styles from '../../Tools/style.less';

const { TextArea, Search } = Input;

export default class ReportsForm extends PureComponent {
  index = 0;

  cacheOriginData = {};

  constructor(props) {
    super(props);

    this.state = {
      data: props.value,
      filters: {
        keyWord: '',
      },
      removeKeys: [],
      removeJsons: [],
    };
  }

  componentWillReceiveProps(nextProps) {
    if ('reportsList' in nextProps && nextProps.reportsList) {
      this.setState({
        data: nextProps.reportsList.data,
      });
    }
  }

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

  getRowByKey(key, newData) {
    const { data } = this.state;
    return (newData || data).filter(item => item.key === key)[0];
  }

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

  handleTableChange = (pagination, filter) => {
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
    search.page = pagination.current;
    search.size = pagination.pageSize;
    this.onSearchChange(search);
  };

  removeRows = () => {
    const { editRows } = this.props;
    const { data, removeKeys, filters, removeJsons } = this.state;
    const newData = data.filter(item => removeKeys.indexOf(item.key) === -1);
    const rowKeys = removeKeys.filter(item => typeof item === 'number');
    this.setState({ data: newData });
    if (rowKeys.length > 0 && removeJsons.length > 0) {
      editRows({ key: rowKeys, jsonFiles: removeJsons }, 'delete', () => {
        this.onSearchChange(filters);
      });
    }
    this.setState({
      removeKeys: [],
      removeJsons: [],
    });
  };

  onSelectChange = (selectedRowKeys, selectedRows) => {
    const { currentUser } = this.props;
    const { removeKeys, removeJsons } = this.state;
    const selected = selectedRows
      .filter(element => currentUser.authority === 'admin' || element.userId === currentUser.userId)
      .map(item => item.key);
    const removeKeysList = selectedRowKeys.filter(
      item => removeKeys.indexOf(item) >= 0 || selected.indexOf(item) >= 0
    );
    selectedRows.forEach(item => {
      if (removeJsons.map(ele => ele.key).indexOf(item.key) < 0) {
        removeJsons.push(item);
      }
    });
    this.setState({
      removeKeys: removeKeysList,
      removeJsons: removeJsons
        .filter(item => removeKeysList.indexOf(item.key) >= 0)
        .map(item => ({ key: item.key, jid: item.jid, date: item.date })),
    });
  };

  remove(record) {
    const { data, filters } = this.state;
    const newData = data.filter(item => item.key !== record.key);
    const { editRows } = this.props;
    this.setState({ data: newData });
    editRows(record, 'delete', () => {
      this.onSearchChange(filters);
    });
  }

  handleKeyPress(e, key) {
    if (e.key === 'Enter') {
      this.saveRow(e, key);
    }
  }

  handleFieldChange(e, fieldName, key) {
    const { data } = this.state;
    const newData = data.map(item => ({ ...item }));
    const target = this.getRowByKey(key, newData);
    if (target) {
      target[fieldName] = e.target ? e.target.value : e;
      this.setState({ data: newData });
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
    if (!target.pid || !target.title || !target.key || target.failCases < 0) {
      message.error('请填写正确的报告信息。');
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
      reportsList: { total, page },
      project: { projectsList, teams },
      currentUser,
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
        width: '10%',
        render: text => text,
      },
      {
        title: '所属组',
        dataIndex: 'team',
        key: 'tid',
        filters: teams.map(item => ({ text: item.name, value: item.tid })),
        width: '8%',
        render: text => text,
      },
      {
        title: '所属项目',
        dataIndex: 'project',
        key: 'pid',
        filters: projectsList.map(item => ({ text: item.name, value: item.pid })),
        width: '10%',
        render: text => text,
      },
      {
        title: '用例数',
        dataIndex: 'runCases',
        key: 'runCases',
        width: '8%',
        render: text => text,
      },
      {
        title: '通过',
        dataIndex: 'passCases',
        key: 'passCases',
        width: '5%',
        render: text => text,
      },
      {
        title: '失败',
        dataIndex: 'failCases',
        key: 'failCases',
        width: '5%',
        render: text => text,
      },
      {
        title: '通过率',
        dataIndex: 'passRate',
        key: 'passRate',
        width: '6%',
        render: text =>
          (text * 100)
            .toFixed(2)
            .toString()
            .concat(' %'),
      },
      {
        title: '耗时(分钟)',
        dataIndex: 'runTime',
        key: 'runTime',
        width: '8%',
        render: text => text,
      },
      {
        title: '状态',
        dataIndex: 'status',
        key: 'status',
        width: '8%',
        filters: [
          { text: '全部通过', value: '2' },
          { text: '部分通过', value: '1' },
          { text: '全部失败', value: '0' },
        ],
        render: text => {
          if (text.toString() === '0') {
            return '全部失败';
          }
          if (text.toString() === '1') {
            return '部分通过';
          }
          return '全部通过';
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
                <a onClick={e => this.toggleEditable(e, record.key)}>编辑</a>
                <Divider type="vertical" />
                <Link to={`/gui/reports/detail/${record.jid}/${record.date}`}>详情</Link>
                <Divider type="vertical" />
                <Popconfirm
                  title="将会删除该报告及详情, 是否继续？"
                  onConfirm={() => this.remove(record)}
                >
                  <a>删除</a>
                </Popconfirm>
              </span>
            );
          }
          return (
            <span>
              <a onClick={e => this.toggleEditable(e, record.key)}>编辑</a>
              <Divider type="vertical" />
              <Link to={`/gui/reports/detail/${record.jid}/${record.date}`}>详情</Link>
            </span>
          );
        },
      },
    ];
    const { removeKeys, data, removeJsons } = this.state;
    const hasSelected = removeKeys.length > 0 && removeJsons.length > 0;
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
          loading={loading}
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
                  {record.runTime}
                  <Divider />
                  <h3>报告描述:</h3>
                  <TextArea
                    value={record.description}
                    onChange={e => this.handleFieldChange(e, 'description', record.key)}
                    placeholder="报告描述"
                    autosize={{ minRows: 5, maxRows: 25 }}
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
                {record.runTime}
                <Divider />
                <h3>报告描述:</h3>
                <TextArea
                  value={record.description}
                  style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
                  placeholder="报告描述"
                  disabled
                  autosize={{ minRows: 5, maxRows: 25 }}
                />
              </Fragment>
            );
          }}
        />
      </Fragment>
    );
  }
}
