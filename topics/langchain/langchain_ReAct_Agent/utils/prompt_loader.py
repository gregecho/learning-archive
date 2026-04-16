from logger_handler import logger
from config_handler import prompts_conf
from path_tool import get_absolute_path


def get_system_prompts():
    try:
        system_prompt_path = get_absolute_path(prompts_conf["main_prompt_path"])
    except KeyError as ke:
        logger.error(f"[system_prompt_path]在yaml配置中没有main_prompt_path")
        raise ke

    try:
        return open(system_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[system_prompt_path]解析系统提示词出错, {str(e)}")
        raise e


def get_report_prompts():
    try:
        report_prompt_path = get_absolute_path(prompts_conf["report_prompt_path"])
    except KeyError as ke:
        logger.error(f"[get_report_prompts]在yaml配置中没有report_prompt_path")
        raise ke

    try:
        return open(report_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[get_report_prompts]解析报告提示词出错, {str(e)}")
        raise e


def get_rag_prompts():
    try:
        rag_summarize_prompt_path = get_absolute_path(
            prompts_conf["rag_summarize_prompt_path"]
        )
    except KeyError as ke:
        logger.error(f"[get_rag_prompts]在yaml配置中没有rag_summarize_prompt_path")
        raise ke

    try:
        return open(rag_summarize_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[get_rag_prompts]解析RAG提示词出错, {str(e)}")
        raise e


if __name__ == "__main__":
    print(get_rag_prompts()[:10])
    print(get_report_prompts()[:10])
    print(get_system_prompts()[:10])
