# Copyright 2025 ZTE Corporation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
CoSight 测试文件，用于本地调试 CoSight 功能
"""
import os
from datetime import datetime
from llm import llm_for_plan, llm_for_act, llm_for_tool, llm_for_vision
from CoSight import CoSight
from app.common.logger_util import logger


def main():
    """主函数，用于测试 CoSight 功能"""
    # 配置工作区路径
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    work_space_path = os.path.join(BASE_DIR, "work_space")
    if not os.path.exists(work_space_path):
        os.makedirs(work_space_path)
    
    # 获取当前时间并格式化
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    # 构造路径：work_space/work_space_时间戳
    work_space_path_time = os.path.join(work_space_path, f'work_space_{timestamp}')
    os.makedirs(work_space_path_time, exist_ok=True)
    
    # 将工作空间路径存储到环境变量，供RecordGenerator使用
    os.environ['WORKSPACE_PATH'] = work_space_path_time
    
    # 生成 plan_id
    plan_id = f"plan_{timestamp}"
    
    logger.info(f"Using work_space_path: {work_space_path_time}")
    logger.info(f"Using plan_id: {plan_id}")
    logger.info(f"llm_for_plan: {llm_for_plan.model}, {llm_for_plan.base_url}, {llm_for_plan.api_key}")
    
    # 初始化 CoSight
    cosight = CoSight(
        llm_for_plan,
        llm_for_act,
        llm_for_tool,
        llm_for_vision,
        work_space_path=work_space_path_time,
        message_uuid=plan_id
    )
    
    # 测试查询内容 - 可以在这里修改测试查询
    query_content = "请告诉我1+1的结果是什么"
    logger.info(f"Starting CoSight execution with query: {query_content}")
    
    # 执行 CoSight
    result = cosight.execute(query_content)
    
    logger.info(f"CoSight execution completed. Final result: {result}")


if __name__ == '__main__':
    main()

