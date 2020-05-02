import React, { PureComponent, Fragment } from 'react';
import { Table, Input, Divider, message, Row, Col, Tag } from 'antd';
import styles from '../Tools/style.less';

const { TextArea, Search } = Input;

export default class BeRunCasesForm extends PureComponent {
  index = 0;

  cacheOriginData = {};

  constructor(props) {
    super(props);

    this.state = {
      exportKeys: [],
      selectedCases: [],
      filters: {
        keyWord: '',
      },
    };
  }

  componentWillReceiveProps() {
    const { visible, selectedCases } = this.props;
    const { exportKeys, selectedCases: cases } = this.state;
    if ((exportKeys.length === 0 || cases.length === 0) && selectedCases.length > 0) {
      this.setState({ exportKeys: selectedCases.map(item => item.key), selectedCases });
    }
    if (!visible) {
      this.setState({ exportKeys: [], selectedCases: [] });
    }
  }

  handleTableChange = pagination => {
    const { filters } = this.state;
    const search = filters;
    search.page = pagination.current;
    search.size = pagination.pageSize;
    this.onSearchChange(search);
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
    const { selectedCases } = this.state;
    const { onSelectCases } = this.props;
    const cases = selectedRows.map(item => ({
      key: item.key,
      cid: item.cid,
      title: item.title,
      function: item.function,
    }));
    const noFunction = selectedRows
      .filter(item => item.function.trim() === '')
      .map(item => item.key);
    if (noFunction.length > 0) {
      message.warn('执行函数不能为空, 已忽略该部分!');
    }
    const selectedKeys = selectedRowKeys.filter(item => !noFunction.includes(item));
    const selectedTestCases = cases.concat(
      selectedCases.filter(item => !cases.map(ele => ele.key).includes(item.key))
    );
    const testCases = selectedTestCases
      .filter(item => selectedKeys.includes(item.key))
      .sort((a, b) => (a.cid > b.cid ? 1 : -1));
    this.setState({
      exportKeys: selectedKeys,
      selectedCases: testCases,
    });
    onSelectCases(testCases);
  };

  render() {
    const {
      loading,
      testCases: { data, total, page },
    } = this.props;
    const columns = [
      {
        title: '#',
        dataIndex: 'no',
        key: 'no',
        width: '5%',
        render: text => text,
      },
      {
        title: '用例编号',
        dataIndex: 'cid',
        key: 'cid',
        width: '15%',
        render: text => text,
      },
      {
        title: '所属组',
        dataIndex: 'team',
        key: 'tid',
        width: '15%',
        render: text => text,
      },
      {
        title: '所属项目',
        dataIndex: 'project',
        key: 'pid',
        width: '15%',
        render: text => text,
      },
      {
        title: '用例标题',
        dataIndex: 'title',
        key: 'title',
        width: '40%',
        render: text => text,
      },
      {
        title: '作者',
        dataIndex: 'author',
        key: 'author',
        width: '10%',
        render: text => text,
      },
    ];
    const { exportKeys, selectedCases } = this.state;
    return (
      <Fragment>
        <Row>
          <Col span={20}>
            <b>已选用例:&nbsp;&nbsp;</b>
            {selectedCases.map(item => (
              <Tag style={{ marginBottom: 10 }} key={item.key} title={item.title}>
                {item.cid}
              </Tag>
            ))}
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
          rowSelection={{
            selections: true,
            selectedRowKeys: exportKeys,
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
          expandedRowRender={record => (
            <Fragment>
              <h3>系统模块:</h3>
              {record.module}
              <Divider />
              <h3>执行函数:</h3>
              {record.function}
              <Divider />
              <h3>用例描述:</h3>
              <TextArea
                value={record.description}
                style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
                placeholder="用例描述"
                disabled
                autosize
              />
              <Divider />
              <h3>预期结果:</h3>
              <TextArea
                value={record.expected}
                style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
                placeholder="预期结果"
                disabled
                autosize
              />
            </Fragment>
          )}
        />
      </Fragment>
    );
  }
}
