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
  Upload,
  Icon,
} from 'antd';
import Link from 'umi/link';
import styles from '../../Tools/style.less';
import makePy from '../../GUITest/TestCase/pinying';

const { TextArea, Search } = Input;
const { Option } = Select;

export default class TestCaseForm extends PureComponent {
  index = 0;

  cacheOriginData = {};

  constructor(props) {
    super(props);

    this.state = {
      data: props.value,
      removeKeys: [],
      exportKeys: [],
      filters: {
        keyWord: '',
      },
      loadings: false,
    };
  }

  componentWillReceiveProps(nextProps) {
    if ('testCases' in nextProps && nextProps.testCases) {
      this.setState({
        data: nextProps.testCases.data,
      });
    }
  }

  onPageChange = (page, pageSize) => {
    const { filters } = this.state;
    const { onPageChange } = this.props;
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
      exportKeys: selectedRowKeys,
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

  removeRows = () => {
    const { editRows } = this.props;
    const { data, removeKeys, exportKeys, filters } = this.state;
    const newData = data.filter(item => removeKeys.indexOf(item.key) === -1);
    const rowKeys = removeKeys.filter(item => typeof item === 'number');
    this.setState({ data: newData });
    if (rowKeys.length > 0) {
      editRows({ key: rowKeys }, 'delete', ()=>{
        this.onSearchChange(filters);
      });
    }
    this.setState({
      removeKeys: [],
      exportKeys: exportKeys.filter(item => removeKeys.indexOf(item) === -1),
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
      module: '',
      pid: '',
      title: '',
      cid: '',
      description: '',
      expected: '',
      actual: '',
      urlCount: '',
      status: 1,
      author: '',
      executor: '',
      function: '',
      userId: currentUser.userId,
      editable: true,
      isNew: true,
    });
    this.index += 1;
    this.setState({ data: newData });
  };

  exportTC = () => {
    const { exportKeys } = this.state;
    const { editRows } = this.props;
    editRows({ sid: exportKeys.filter(item => typeof item === 'number') }, 'export');
  };

  downloadTCT = () => {
    const { editRows } = this.props;
    editRows({ sid: [] }, 'template');
  };

  beforeUpload = file => {
    const isXlsx =
      file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
    if (!isXlsx) {
      message.error('请上传xlsx格式的文件!');
    }
    const isLt50M = file.size / 1024 / 1024 < 50;
    if (!isLt50M) {
      message.error('文件大小必须小于50M!');
    }
    return isXlsx && isLt50M;
  };

  handleChange = info => {
    const { filters } = this.state;
    if (info.file.status === 'uploading') {
      this.setState({ loadings: true });
      return;
    }
    if (info.file.status === 'done') {
      this.setState({
        loadings: false,
      });
      if (info.file.response.status === 'SUCCESS') {
        message.success(info.file.response.message);
        this.onSearchChange(filters);
      } else {
        message.error(info.file.response.message);
      }
    } else if (info.file.status === 'error') {
      if (info.file.response) {
        message.error(info.file.response.message);
      } else {
        message.error('文件上传失败!');
      }
      this.setState({
        loadings: false,
      });
    }
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

  handleKeyPress(e, key) {
    if (e.key === 'Enter') {
      this.saveRow(e, key);
    }
  }

  handleFieldChange(e, fieldName, key) {
    const {
      value,
      project: { projectsList },
      testCases: { total, size, page },
    } = this.props;
    const { data } = this.state;
    const newData = data.map(item => ({ ...item }));
    const target = this.getRowByKey(key, newData);
    const oldCid = value.filter(item => item.key === target.key);
    if (target) {
      const tValue = e.target ? e.target.value : e;
      target[fieldName] = tValue;
      if (fieldName === 'pid') {
        let num;
        if (typeof target.no === 'number') {
          num = target.no;
        } else if (total / size > page) {
          num = total - size + newData.length;
        } else {
          num = newData.length + page * size - size;
        }
        num = num.toString();
        target.project = projectsList.filter(item => item.pid === tValue)[0].name;
        target.cid =
          typeof target.key === 'number' && target.cid && oldCid.length > 0 && oldCid[0].cid
            ? target.cid
            : makePy(target.project)
                .join('')
                .concat('_')
                .concat('00000'.substring(0, '00000'.length - num.length) + num);
      }
      this.setState({ data: newData });
    }
  }

  remove(record) {
    const { data, filters, removeKeys, exportKeys } = this.state;
    const newData = data.filter(item => item.key !== record.key);
    const { editRows } = this.props;
    this.setState({ data: newData });
    if (typeof record.key === 'number') {
      editRows(record, 'delete', ()=>{
        this.onSearchChange(filters);
      });
    }
    this.setState({
      removeKeys: removeKeys.filter(item => item !== record.key),
      exportKeys: exportKeys.filter(item => item !== record.key),
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
    if (!target.pid || !target.title) {
      message.error('请填写完整的用例信息。');
      e.target.focus();
      return;
    }
    this.toggleEditable(e, key);
    const { filters } = this.state;
    editRows(target, 'edit', ()=>{
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
      testCases: { total, page },
      project: { projectsList, teams },
      currentUser,
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
        title: '用例编号',
        dataIndex: 'cid',
        key: 'cid',
        width: '8%',
        render: text => text,
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
        title: '用例标题',
        dataIndex: 'title',
        key: 'title',
        width: '20%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                value={text}
                autoFocus
                onChange={e => this.handleFieldChange(e, 'title', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="用例标题"
              />
            );
          }
          return text;
        },
      },
      {
        title: '接口数量',
        dataIndex: 'urlCount',
        key: 'urlCount',
        width: '6%',
        render: text => text,
      },
      {
        title: '状态',
        dataIndex: 'status',
        key: 'status',
        width: '6%',
        filters: [
          { text: '已实现', value: '2' },
          { text: '开发中', value: '1' },
          { text: '已废弃', value: '0' },
        ],
        render: (text, record) => {
          if (record.editable) {
            return (
              <Select
                defaultValue={text.toString()}
                value={text.toString()}
                onChange={e => this.handleFieldChange(e, 'status', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="状态"
              >
                <Option value="2">已实现</Option>
                <Option value="1">开发中</Option>
                <Option value="0">已废弃</Option>
              </Select>
            );
          }
          if (text.toString() === '0') {
            return '已废弃';
          }
          if (text.toString() === '1') {
            return '开发中';
          }
          return '已实现';
        },
      },
      {
        title: '作者',
        dataIndex: 'author',
        key: 'author',
        width: '7%',
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
                <a onClick={e => this.toggleEditable(e, record.key)}>编辑</a>
                <Divider type="vertical" />
                <Link to={`/api/testcase/detail/${record.pid}/${record.cid}`}>详情</Link>
                <Divider type="vertical" />
                <Popconfirm
                  title="将会删除该用例相关的所有信息, 是否要删除此行？"
                  onConfirm={() => this.remove(record)}
                >
                  <a>删除</a>
                </Popconfirm>
              </span>
            );
          }
          return (
            <span>
              <Link to={`/api/testcase/detail/${record.pid}/${record.cid}`}>详情</Link>
            </span>
          );
        },
      },
    ];
    const { removeKeys, exportKeys, loadings, data } = this.state;
    const hasSelected = removeKeys.length > 0;
    const hasESelected = exportKeys.length > 0;
    return (
      <Fragment>
        <Row>
          <Col span={20}>
            <Upload
              name="testCase"
              showUploadList={false}
              action="/api/py/upload/files/testCase"
              data={{ test_type: 'caseA' }}
              accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
              beforeUpload={this.beforeUpload}
              onChange={this.handleChange}
            >
              <Button type="primary" loading={loadings}>
                <Icon type="upload" />
                批量导入
              </Button>
            </Upload>
            <Divider type="vertical" />
            <Button
              type="primary"
              disabled={!hasESelected}
              loading={hasESelected && loading}
              onClick={this.exportTC}
            >
              <Icon type="download" />
              批量导出
            </Button>
            <Divider type="vertical" />
            <Popconfirm
              title="将会删除所选用例相关的所有信息, 是否要删除？"
              onConfirm={() => this.removeRows()}
            >
              <Button type="primary" disabled={!hasSelected}>
                <Icon type="delete" />
                批量删除
              </Button>
            </Popconfirm>
            <Divider type="vertical" />
            <a onClick={this.downloadTCT}>下载用例模板</a>
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
          pagination={false}
          onChange={this.handleTableChange}
          rowClassName={record => (record.editable ? styles.editable : '')}
          expandedRowRender={record => {
            if (record.editable) {
              return (
                <Fragment>
                  <h3>系统模块:</h3>
                  <Input
                    value={record.module}
                    autoFocus
                    onChange={e => this.handleFieldChange(e, 'module', record.key)}
                    onKeyPress={e => this.handleKeyPress(e, record.key)}
                    placeholder="系统模块"
                  />
                  <Divider />
                  <h3>执行函数:</h3>
                  <Input
                    value={record.function}
                    autoFocus
                    onChange={e => this.handleFieldChange(e, 'function', record.key)}
                    onKeyPress={e => this.handleKeyPress(e, record.key)}
                    placeholder="执行函数"
                  />
                  <Divider />
                  <h3>用例描述:</h3>
                  <TextArea
                    value={record.description}
                    onChange={e => this.handleFieldChange(e, 'description', record.key)}
                    placeholder="用例描述"
                    autosize
                  />
                  <Divider />
                  <h3>预期结果:</h3>
                  <TextArea
                    value={record.expected}
                    onChange={e => this.handleFieldChange(e, 'expected', record.key)}
                    placeholder="预期结果"
                    autosize
                  />
                </Fragment>
              );
            }
            return (
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
            );
          }}
        />
        <Button
          style={{ width: '100%', marginTop: 16, marginBottom: 8 }}
          type="dashed"
          onClick={this.newMember}
          icon="plus"
        >
          新增用例
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
      </Fragment>
    );
  }
}
