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
} from 'antd';
import styles from '../style.less';

const { TextArea, Search } = Input;
const { Option } = Select;

export default class ToolsForm extends PureComponent {
  index = 0;

  cacheOriginData = {};

  constructor(props) {
    super(props);

    this.state = {
      data: props.value,
    };
  }

  componentWillReceiveProps(nextProps) {
    if ('newData' in nextProps) {
      this.setState({
        data: nextProps.newData,
      });
    }
  }

  onPageChange = (page, pageSize) => {
    const { onPageChange } = this.props;
    onPageChange(page, pageSize);
  };

  onShowSizeChange = (current, size) => {
    const { onShowSizeChange } = this.props;
    onShowSizeChange(current, size);
  };

  onSearch = data => {
    const { onSearch } = this.props;
    onSearch(data);
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

  newMember = () => {
    const { currentUser } = this.props;
    const { data } = this.state;
    const newData = data.map(item => ({ ...item }));
    newData.push({
      key: `NEW_TEMP_ID_${this.index}`,
      name: '',
      tid: '',
      description: '',
      link: '',
      status: '1',
      userId: currentUser.userId,
      editable: true,
      isNew: true,
    });
    this.index += 1;
    this.setState({ data: newData });
  };

  remove(record) {
    const { data } = this.state;
    const { removeRow } = this.props;
    const newData = data.filter(item => item.key !== record.key);
    this.setState({ data: newData });
    if (typeof record.tid === 'number') {
      removeRow(record);
    }
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
    e.persist();

    if (this.clickedCancel) {
      this.clickedCancel = false;
      return;
    }
    const target = this.getRowByKey(key) || {};
    if (!target.name || !target.status) {
      message.error('请填写完整的工具信息。');
      e.target.focus();
      return;
    }
    this.toggleEditable(e, key);
    const { saveRow } = this.props;
    saveRow(target);
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
    const { currentUser, page, total, loading } = this.props;
    const { data } = this.state;
    const columns = [
      {
        title: '#',
        dataIndex: 'key',
        key: 'key',
        width: '5%',
        render: text => text,
      },
      {
        title: '工具编号',
        dataIndex: 'tid',
        key: 'tid',
        width: '8%',
        render: text => text,
      },
      {
        title: '工具名称',
        dataIndex: 'name',
        key: 'name',
        width: '15%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                value={text}
                autoFocus
                onChange={e => this.handleFieldChange(e, 'name', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="工具名称"
              />
            );
          }
          return text;
        },
      },
      {
        title: '工具描述',
        dataIndex: 'description',
        key: 'description',
        width: '25%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <TextArea
                value={text}
                onChange={e => this.handleFieldChange(e, 'description', record.key)}
                placeholder="工具描述"
              />
            );
          }
          return (
            <TextArea
              value={text}
              style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
              placeholder="工具描述"
              disabled
            />
          );
        },
      },
      {
        title: '工具链接',
        dataIndex: 'link',
        key: 'link',
        width: '25%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                value={text}
                onChange={e => this.handleFieldChange(e, 'link', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="工具链接"
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
        width: '10%',
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
                <Option value="1">启用</Option>
                <Option value="0">禁用</Option>
              </Select>
            );
          }
          return text.toString() === '1' ? '启用' : '禁用';
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
                <a onClick={e => this.toggleEditable(e, record.key)}>编辑</a>
                <Divider type="vertical" />
                <Popconfirm
                  title="统计数据将被清空, 是否要删除此行？"
                  onConfirm={() => this.remove(record)}
                >
                  <a>删除</a>
                </Popconfirm>
              </span>
            );
          }
          return <span>无权限</span>;
        },
      },
    ];

    return (
      <Fragment>
        <Row>
          <Col span={4} offset={20}>
            <Search
              style={{ marginBottom: 20 }}
              placeholder="按工具名称搜索"
              onSearch={this.onSearch}
              enterButton
            />
          </Col>
        </Row>
        <Table
          loading={loading}
          columns={columns}
          dataSource={data}
          pagination={false}
          rowClassName={record => (record.editable ? styles.editable : '')}
        />
        <Button
          style={{ width: '100%', marginTop: 16, marginBottom: 8 }}
          type="dashed"
          onClick={this.newMember}
          icon="plus"
        >
          新增工具
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
