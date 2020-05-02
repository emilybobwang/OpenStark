import React, { PureComponent, Fragment } from 'react';
import { Table, Button, Input, message, Divider, Row, Col, Icon } from 'antd';
import { goBack } from 'umi/router';
import styles from '../../Tools/style.less';

const { TextArea, Search } = Input;

export default class DetailForm extends PureComponent {
  index = 0;

  cacheOriginData = {};

  constructor(props) {
    super(props);

    this.state = {
      data: props.value,
      filters: {
        keyWord: '',
      },
    };
  }

  componentWillReceiveProps(nextProps) {
    if ('detailList' in nextProps && nextProps.detailList) {
      this.setState({
        data: nextProps.detailList.data,
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
    if (Object.keys(filter).includes('result')) {
      search.result = filter.result.join(',');
    }
    search.page = pagination.current;
    search.size = pagination.pageSize;
    this.onSearchChange(search);
  };

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
    if (!target.cid || !target.description) {
      message.error('请填写正确的备注信息。');
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
      detailList: { total, page },
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
        title: '用例编号',
        dataIndex: 'cid',
        key: 'cid',
        width: '8%',
        render: text => text,
      },
      {
        title: '用例标题',
        dataIndex: 'title',
        key: 'title',
        width: '20%',
        render: text => text,
      },
      {
        title: '执行次数',
        dataIndex: 'runTimes',
        key: 'runTimes',
        width: '6%',
        render: text => text,
      },
      {
        title: '通过次数',
        dataIndex: 'passTimes',
        key: 'passTimes',
        width: '6%',
        render: text => text,
      },
      {
        title: '通过率',
        dataIndex: 'runPassRate',
        key: 'runPassRate',
        width: '6%',
        render: text =>
          (text * 100)
            .toFixed(2)
            .toString()
            .concat(' %'),
      },
      {
        title: '最大耗时(秒)',
        dataIndex: 'maxRunTime',
        key: 'maxRunTime',
        width: '8%',
        render: text => text,
      },
      {
        title: '最小耗时(秒)',
        dataIndex: 'minRunTime',
        key: 'minRunTime',
        width: '8%',
        render: text => text,
      },
      {
        title: '平均耗时(秒)',
        dataIndex: 'avgRunTime',
        key: 'avgRunTime',
        width: '8%',
        render: text => text,
      },
      {
        title: '结果',
        dataIndex: 'result',
        key: 'result',
        width: '8%',
        filters: [
          { text: 'PASS', value: 'PASS' },
          { text: 'FAIL', value: 'FAIL' },
          { text: 'ERROR', value: 'ERROR' },
        ],
        render: text => text,
      },
      {
        title: '执行者',
        dataIndex: 'executor',
        key: 'executor',
        width: '7%',
        render: text => text,
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
              </span>
            );
          }
          return <span>无权限</span>;
        },
      },
    ];
    const { data } = this.state;
    return (
      <Fragment>
        <Row>
          <Col span={20}>
            <Button type="primary" onClick={goBack}>
              <Icon type="rollback" />
              返回
            </Button>
          </Col>
          <Col span={4}>
            <Search
              style={{ marginBottom: 20 }}
              placeholder="按用例编号/标题/描述搜索"
              onSearch={this.onSearchChange}
              enterButton
            />
          </Col>
        </Row>
        <Table
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
                  <h3>最近一次执行情况:</h3>
                  开始时间:&nbsp;&nbsp;
                  {record.startTime}
                  <Divider type="vertical" />
                  结束时间:&nbsp;&nbsp;
                  {record.endTime}
                  <Divider type="vertical" />
                  执行耗时(秒):&nbsp;&nbsp;
                  {record.runTime}
                  <Divider type="vertical" />
                  测试结果:&nbsp;&nbsp;
                  {record.lastResult}
                  <Divider />
                  <h3>实际结果:</h3>
                  <TextArea
                    value={record.actual}
                    style={{
                      backgroundColor: '#fff',
                      color: 'rgba(0, 0, 0, 0.65)',
                    }}
                    placeholder="实际结果"
                    autosize={{ minRows: 5, maxRows: 25 }}
                    disabled
                  />
                  <Divider />
                  <h3>备注:</h3>
                  <TextArea
                    value={record.description}
                    onChange={e => this.handleFieldChange(e, 'description', record.key)}
                    placeholder="备注"
                    autosize={{ minRows: 5, maxRows: 25 }}
                  />
                </Fragment>
              );
            }
            return (
              <Fragment>
                <h3>最近一次执行情况:</h3>
                开始时间:&nbsp;&nbsp;
                {record.startTime}
                <Divider type="vertical" />
                结束时间:&nbsp;&nbsp;
                {record.endTime}
                <Divider type="vertical" />
                执行耗时(秒):&nbsp;&nbsp;
                {record.runTime}
                <Divider type="vertical" />
                测试结果:&nbsp;&nbsp;
                {record.lastResult}
                <Divider />
                <h3>实际结果:</h3>
                <TextArea
                  value={record.actual}
                  style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
                  placeholder="实际结果"
                  autosize={{ minRows: 5, maxRows: 25 }}
                  disabled
                />
                <Divider />
                <h3>备注:</h3>
                <TextArea
                  value={record.description}
                  style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
                  placeholder="备注"
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
