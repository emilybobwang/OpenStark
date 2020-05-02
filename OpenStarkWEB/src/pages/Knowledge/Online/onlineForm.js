import React, { PureComponent, Fragment } from 'react';
import {
  Table,
  Button,
  Input,
  Popconfirm,
  Divider,
  Row,
  Col,
  Pagination,
  Icon,
  Modal,
  message,
  DatePicker,
} from 'antd';
import BraftEditor, { EditorState } from 'braft-editor';
import 'braft-editor/dist/index.css';
import moment from 'moment';
import styles from '../../Tools/style.less';

const { TextArea, Search } = Input;
const { RangePicker } = DatePicker;

export default class OnlineForm extends PureComponent {
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
        startTime: '',
        endTime: '',
      },
      visible: false,
      content: '',
    };
  }

  componentWillReceiveProps(nextProps) {
    if ('online' in nextProps && nextProps.online) {
      this.setState({
        data: nextProps.online.data,
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
      exportKeys: selectedRowKeys,
    });
  };

  removeRows = () => {
    const { editRows } = this.props;
    const { data, removeKeys, filters, exportKeys } = this.state;
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

  handleRangePickerChange = rangePickerValue => {
    const { filters } = this.state;
    const keyWords = filters;
    keyWords.startTime =
      rangePickerValue.length > 1 ? rangePickerValue[0].format('YYYY-MM-DD') : '';
    keyWords.endTime = rangePickerValue.length > 1 ? rangePickerValue[1].format('YYYY-MM-DD') : '';
    this.setState({
      filters: keyWords,
    });
    this.onSearchChange(keyWords);
  };

  handleTableChange = (_, filter) => {
    const { filters } = this.state;
    const search = filters;
    if (Object.keys(filter).includes('severity')) {
      search.severity = filter.severity.join(',');
    }
    if (Object.keys(filter).includes('tid')) {
      search.tid = filter.tid.join(',');
    }
    if (Object.keys(filter).includes('status')) {
      search.status = filter.status.join(',');
    }
    this.onSearchChange(search);
  };

  handleOk = () => {
    const { sendMail } = this.props;
    const { content } = this.state;
    if (content) {
      sendMail({ content });
      this.setState({
        visible: false,
      });
    } else {
      message.error('邮件内容不能为空!');
      this.setState({
        visible: false,
      });
    }
  };

  handleCancel = () => {
    this.setState({
      visible: false,
    });
  };

  showModal = () => {
    const { data, exportKeys } = this.state;
    let mailData = [];
    const keys = {
      foundTime: '发现日期',
      team: '所属组',
      severity: '严重程度',
      module: '功能模块',
      requirement: '对应需求',
      publishTime: '发布日期',
      principal: '责任人',
      bug: '线上bug描述',
      effect: '问题影响',
      solution: '问题处理',
      attribution: '缺陷归属',
      cause: '原因分析',
      answer: '测试规避措施',
      analyzeTime: '分析日期',
      status: '状态',
      closeTime: '关闭日期',
      remarks: '备注',
    };
    mailData = data.filter(item => exportKeys.includes(item.key));
    let content = '<p style="font-size: 16px;"><b>日期: '
      .concat(moment(new Date(), 'YYYY-MM-DD').format('YYYY-MM-DD HH:mm:ss'))
      .concat('</b></p>');
    let no = 0;
    mailData.forEach(item => {
      no += 1;
      content = content
        .concat('<p style="font-size: 16px;"><b>问题 ')
        .concat(no)
        .concat(
          ':</b></p><table style="width: 1030px; border: solid 1px #c5c5c5; font-size: 16px;">'
        );
      Object.keys(item).forEach(ele => {
        if (Object.keys(keys).includes(ele)) {
          if (['bug', 'cause', 'answer'].includes(ele)) {
            const itemValue = item[ele];
            Object.keys(item[ele].entityMap).forEach(key => {
              const uri = item[ele].entityMap[key].data.url;
              itemValue.entityMap[key].data.url = uri.startsWith('http')
                ? uri
                : window.location.origin.concat(uri);
            });
            content = content
              .concat(
                '<tr><th style="width: 150px; border: solid 1px #c5c5c5; background-color: lavender;">'
              )
              .concat(keys[ele])
              .concat('</th><td style="border: solid 1px #c5c5c5; background-color: lavender;">')
              .concat(EditorState.createFrom(itemValue).toHTML())
              .concat('</td></tr>');
          } else if (ele === 'status') {
            content = content
              .concat(
                '<tr><th style="width: 150px; border: solid 1px #c5c5c5; background-color: lavender;">'
              )
              .concat(keys[ele])
              .concat('</th><td style="border: solid 1px #c5c5c5; background-color: lavender;">')
              .concat(item[ele] === 1 ? '打开' : '关闭')
              .concat('</td></tr>');
          } else {
            content = content
              .concat(
                '<tr><th style="width: 150px; border: solid 1px #c5c5c5; background-color: lavender;">'
              )
              .concat(keys[ele])
              .concat('</th><td style="border: solid 1px #c5c5c5; background-color: lavender;">')
              .concat(item[ele] || '无')
              .concat('</td></tr>');
          }
        }
      });
      content = content.concat('</table>').concat('</br></br>');
    });
    this.setState({
      visible: true,
      content,
    });
  };

  handleKeyPress(e, key) {
    if (e.key === 'Enter') {
      this.saveRow(e, key);
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

  render() {
    const {
      loading,
      online: { total, page },
      teams,
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
        title: '发现日期',
        dataIndex: 'foundTime',
        key: 'foundTime',
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
        title: '严重程度',
        dataIndex: 'severity',
        key: 'severity',
        filters: ['提示', '轻微', '一般', '严重', '致命'].map(item => ({
          text: item,
          value: item,
        })),
        width: '8%',
        render: text => text,
      },
      {
        title: '功能模块',
        dataIndex: 'module',
        key: 'module',
        width: '10%',
        render: text => text,
      },
      {
        title: '对应需求',
        dataIndex: 'requirement',
        key: 'requirement',
        width: '20%',
        render: text => (
          <TextArea
            value={text}
            style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
            placeholder="对应需求"
            disabled
            autosize
          />
        ),
      },
      {
        title: '发布日期',
        dataIndex: 'publishTime',
        key: 'publishTime',
        width: '8%',
        render: text => text,
      },
      {
        title: '责任人',
        dataIndex: 'principal',
        key: 'principal',
        width: '7%',
        render: text => text,
      },
      {
        title: '状态',
        dataIndex: 'status',
        key: 'status',
        width: '6%',
        filters: [{ text: '关闭', value: '0' }, { text: '打开', value: '1' }],
        render: text => (text.toString() === '1' ? '打开' : '关闭'),
      },
      {
        title: '操作',
        key: 'action',
        render: (text, record) => {
          if (!!record.editable && loading) {
            return null;
          }
          if (currentUser.authority === 'admin' || currentUser.userId === record.userId) {
            return (
              <span>
                <a href={`/knowledge/online/edit/${record.key}`}>编辑</a>
                <Divider type="vertical" />
                <Popconfirm title="确定要删除此行？" onConfirm={() => this.remove(record)}>
                  <a>删除</a>
                </Popconfirm>
              </span>
            );
          }
          return <span>无权限</span>;
        },
      },
    ];
    const { removeKeys, data, visible, exportKeys, content } = this.state;
    const hasSelected = removeKeys.length > 0;
    const hasESelected = exportKeys.length > 0;
    const expandedRowRender = record => (
      <Fragment>
        <h3>分析日期:</h3>
        {record.analyzeTime}
        <Divider />
        <h3>线上bug描述:</h3>
        <BraftEditor
          style={{
            border: '1px solid #d9d9d9',
            backgroundColor: '#fff',
            color: 'rgba(0, 0, 0, 0.65)',
          }}
          defaultValue={EditorState.createFrom(record.bug)}
          placeholder="线上bug描述"
        />
        <Divider />
        <h3>问题影响:</h3>
        <TextArea
          value={record.effect}
          style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
          placeholder="问题影响"
          disabled
          autosize
        />
        <Divider />
        <h3>问题处理:</h3>
        <TextArea
          value={record.solution}
          style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
          placeholder="问题处理"
          disabled
          autosize
        />
        <Divider />
        <h3>缺陷归属:</h3>
        {record.attribution}
        <Divider />
        <h3>原因分析:</h3>
        <BraftEditor
          style={{
            border: '1px solid #d9d9d9',
            backgroundColor: '#fff',
            color: 'rgba(0, 0, 0, 0.65)',
          }}
          defaultValue={EditorState.createFrom(record.cause)}
          placeholder="原因分析"
        />
        <Divider />
        <h3>测试规避措施:</h3>
        <BraftEditor
          style={{
            border: '1px solid #d9d9d9',
            backgroundColor: '#fff',
            color: 'rgba(0, 0, 0, 0.65)',
          }}
          defaultValue={EditorState.createFrom(record.answer)}
          placeholder="测试规避措施"
        />
        <Divider />
        <h3>关闭日期:</h3>
        {record.closeTime}
        <Divider />
        <h3>备注:</h3>
        <TextArea
          value={record.remarks}
          style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
          placeholder="备注"
          disabled
          autosize
        />
      </Fragment>
    );

    return (
      <Fragment>
        <Row>
          <Col span={16}>
            <Button icon="plus" type="primary" href="/knowledge/online/edit/NEW_TEMP_KEY">
              新增问题
            </Button>
            <Divider type="vertical" />
            <Popconfirm title="确定要删除？" onConfirm={() => this.removeRows()}>
              <Button type="primary" disabled={!hasSelected}>
                <Icon type="delete" />
                批量删除
              </Button>
            </Popconfirm>
            <Divider type="vertical" />
            <Button
              type="primary"
              disabled={!hasESelected}
              loading={hasESelected && loading}
              onClick={this.showModal}
            >
              <Icon type="mail" />
              发送邮件
            </Button>
          </Col>
          <Col span={4}>
            <RangePicker
              onChange={this.handleRangePickerChange}
              style={{ width: 245 }}
              placeholder={['发现开始日期', '发现结束日期']}
            />
          </Col>
          <Col span={4}>
            <Search
              style={{ marginBottom: 20 }}
              placeholder="按问题内容/责任人搜索"
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
          expandedRowRender={expandedRowRender}
        />
        <a href="/knowledge/online/edit/NEW_TEMP_KEY">
          <Button
            style={{ width: '100%', marginTop: 16, marginBottom: 8 }}
            type="dashed"
            icon="plus"
          >
            新增问题
          </Button>
        </a>
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
          title="邮件预览"
          visible={visible}
          onOk={this.handleOk}
          confirmLoading={loading}
          onCancel={this.handleCancel}
          width={1080}
        >
          <div 
            // eslint-disable-next-line react/no-danger
            dangerouslySetInnerHTML={{ __html: content }} 
          />
        </Modal>
      </Fragment>
    );
  }
}
