import os
from abc import ABC, abstractmethod
import openai
import toml
import json
import requests
import google.generativeai as genai
import re

api_config_path = '/data/yangzhao/uno/Agent/config.toml'


def validate_mag_format(msg):
    if not isinstance(msg, dict):
        raise ValueError("Each message should be a dictionary. ")

    if "role" not in msg or "content" not in msg:
        raise ValueError("Each message dictionary should contain 'role' and 'content' keys. ")

    allowed_roles = ["user", "assistant", "system"]
    if msg["role"] not in allowed_roles:
        raise ValueError("Invalid role in message. Allowed roles are 'user', 'assistant', and 'system'. ")

    if not isinstance(msg['content'], str):
        raise ValueError("Invalid content in message. The content should be a str. ")


def get_api_config(api_name: str) -> dict:
    API_dict = {}
    config = toml.load(api_config_path)
    api_base = config[api_name]['api_base']
    if api_base != 'N/A':
        API_dict['address'] = api_base
    else:
        API_dict['address'] = None
    api_key = config[api_name]['api_key']
    if api_key != 'N/A':
        API_dict['api_key'] = api_key
    else:
        API_dict['api_key'] = None
    organization = config[api_name]['organization']
    if organization != 'N/A':
        API_dict['organization'] = organization
    else:
        API_dict['organization'] = None
    return API_dict


class LLMAgent(ABC):
    def __init__(self, model_category: str):
        config = toml.load(api_config_path)
        self.GPT3_LIST = config['GPT3']['model_list']
        self.GPT4_LIST = config['GPT4']['model_list']
        self.Gemini_LIST = config['Gemini']['model_list']
        self.Llama2_LIST = config['Llama2']['model_list']
        self.GLM3_LIST = config['GLM3']['model_list']
        self.Mistral_LIST = config['Mistral']['model_list']
        self.Gemma_LIST = config['Gemma']['model_list']
        self.MODEL_LIST = (self.GPT3_LIST + self.GPT4_LIST + self.Gemini_LIST +
                           self.Llama2_LIST + self.GLM3_LIST + self.Mistral_LIST + self.Gemma_LIST)
        if model_category not in self.MODEL_LIST:
            raise ValueError(f"wrong category: {model_category}. ")
        self.model_class = model_category
        self.API_module = None
        self.API_config = None
        self.chat = list()

    @abstractmethod
    def sse_invoke(self, msg: dict, temperature=float(0), **model_args) -> str:
        pass


class GPT3Agent(LLMAgent):
    def __init__(self, model_category: str):
        super().__init__(model_category)
        if model_category in self.GPT3_LIST:
            self.model_class = 'GPT3'
            self.API_module = openai
            self.model_category = model_category
        else:
            raise AttributeError('wrong category: ' + model_category)

    def sse_invoke(self, msg: dict, temperature=float(0), **model_args) -> tuple:
        validate_mag_format(msg)
        self.API_config = get_api_config(api_name=self.model_class)
        address = self.API_config['address']
        api_key = self.API_config['api_key']
        if address is not None:
            self.API_module.api_base = address
        if api_key is not None:
            self.API_module.api_key = api_key
        else:
            raise ValueError('the api key of ' + self.model_class + " is None. ")
        response = self.API_module.ChatCompletion.create(
            model=self.model_category,
            messages=[msg],
            temperature=temperature,
            seed=3407,
            **model_args
        )
        return response['choices'][0]['message']['content'], response['usage']


class GPT3Agent_chat(LLMAgent):
    def __init__(self, model_category: str):
        super().__init__(model_category)
        if model_category in self.GPT3_LIST:
            self.model_class = 'GPT3'
            self.API_module = openai
            self.model_category = model_category
        else:
            raise AttributeError('wrong category: ' + model_category)

    def sse_invoke(self, msg: dict, temperature=float(0), **model_args) -> tuple:
        validate_mag_format(msg)
        self.API_config = get_api_config(api_name=self.model_class)
        address = self.API_config['address']
        api_key = self.API_config['api_key']
        if address is not None:
            self.API_module.api_base = address
        if api_key is not None:
            self.API_module.api_key = api_key
        else:
            raise ValueError('the api key of ' + self.model_class + " is None. ")
        self.chat.append(msg)
        response = self.API_module.ChatCompletion.create(
            model=self.model_category,
            messages=self.chat,
            temperature=temperature,
            seed=3407,
            **model_args
        )
        self.chat.append(dict(response['choices'][0]['message']))
        return response['choices'][0]['message']['content'], response['usage']


class GPT4Agent(LLMAgent):
    def __init__(self, model_category: str):
        super().__init__(model_category)
        if model_category in self.GPT4_LIST:
            self.model_class = 'GPT4'
            self.API_module = openai
            self.model_category = model_category
        else:
            raise AttributeError('wrong category: ' + model_category)

    def sse_invoke(self, msg: dict, temperature=float(0), **model_args) -> tuple:
        validate_mag_format(msg)
        self.API_config = get_api_config(api_name=self.model_class)
        address = self.API_config['address']
        api_key = self.API_config['api_key']
        if address is not None:
            self.API_module.api_base = address
        if api_key is not None:
            self.API_module.api_key = api_key
        else:
            raise ValueError('the api key of ' + self.model_class + " is none.")
        response = self.API_module.ChatCompletion.create(
            model=self.model_category,
            messages=[msg],
            temperature=temperature,
            **model_args
        )
        return response['choices'][0]['message']['content'], response['usage']


class GPT4Agent_chat(LLMAgent):
    def __init__(self, model_category: str):
        super().__init__(model_category)
        if model_category in self.GPT4_LIST:
            self.model_class = 'GPT4'
            self.API_module = openai
            self.model_category = model_category
        else:
            raise AttributeError('wrong category: ' + model_category)

    def sse_invoke(self, msg: dict, temperature=float(0), **model_args) -> tuple:
        # os.environ["http_proxy"] = "http://localhost:7890"
        # os.environ["https_proxy"] = "http://localhost:7890"
        validate_mag_format(msg)
        self.API_config = get_api_config(api_name=self.model_class)
        address = self.API_config['address']
        api_key = self.API_config['api_key']
        if address is not None:
            self.API_module.api_base = address
        if api_key is not None:
            self.API_module.api_key = api_key
        else:
            raise ValueError('the api key of ' + self.model_class + " is none.")
        self.chat.append(msg)
        print(api_key)
        response = self.API_module.ChatCompletion.create(
            model=self.model_category,
            messages=self.chat,
            temperature=temperature,
            **model_args
        )
        self.chat.append(dict(response['choices'][0]['message']))
        return response['choices'][0]['message']['content'], response['usage']


class GeminiAgent(LLMAgent):
    def __init__(self, model_category: str):
        super().__init__(model_category)
        if model_category in self.Gemini_LIST:
            self.model_class = 'Gemini'
            self.model_category = model_category
        else:
            raise AttributeError('wrong category: ' + model_category)

    def sse_invoke(self, msg: dict, temperature=float(0), **model_args) -> tuple:
        validate_mag_format(msg)
        self.API_config = get_api_config(api_name=self.model_class)
        address = self.API_config['address']
        data = {
            "messages": msg,
            "temperature": temperature
        }
        result = eval(requests.post(address, data=json.dumps(data)).text)
        return result, None


class GeminiAgent_chat(LLMAgent):
    def __init__(self, model_category: str):
        super().__init__(model_category)
        if model_category in self.Gemini_LIST:
            self.model_class = 'Gemini'
            self.model_category = model_category
            self.chat_model = None
        else:
            raise AttributeError('wrong category: ' + model_category)

    def sse_invoke(self, msg: dict, temperature=float(0), **model_args) -> tuple:
        os.environ["http_proxy"] = "http://localhost:7890"
        os.environ["https_proxy"] = "http://localhost:7890"
        validate_mag_format(msg)
        self.API_config = get_api_config(api_name=self.model_class)
        api_key = self.API_config['api_key']
        if api_key is None:
            raise ValueError('the api key of ' + self.model_class + " is none.")
        if self.chat_model:
            config = genai.GenerationConfig(temperature=temperature)
            response = self.chat_model.send_message(msg['content'], generation_config=config)
        else:
            genai.configure(api_key=api_key)
            gen_model = genai.GenerativeModel(model_name=self.model_category)
            self.chat_model = gen_model.start_chat()
            config = genai.GenerationConfig(temperature=temperature)
            response = self.chat_model.send_message(msg['content'], generation_config=config)
        return response.text, None


class LLAMA2Agent(LLMAgent):
    def __init__(self, model_category: str):
        super().__init__(model_category)
        if model_category in self.Llama2_LIST:
            self.model_class = 'Llama2'
            self.model_category = model_category
        else:
            raise AttributeError('wrong category: ' + model_category)

    def sse_invoke(self, msg: dict, temperature=float(0), **model_args) -> tuple:
        validate_mag_format(msg)
        self.API_config = get_api_config(api_name=self.model_class)
        address = self.API_config['address']
        if address is None:
            raise ValueError('the api address of ' + self.model_class + " is none.")
        history = [msg]
        data = {
            "messages": history,
            "temperature": temperature
        }
        return eval(requests.post(address, data=json.dumps(data)).text), None


class LLAMA2Agent_chat(LLMAgent):
    def __init__(self, model_category: str):
        super().__init__(model_category)
        if model_category in self.Llama2_LIST:
            self.model_class = 'Llama2'
            self.model_category = model_category
        else:
            raise AttributeError('wrong category: ' + model_category)

    def sse_invoke(self, msg: dict, temperature=float(0), **model_args) -> tuple:
        validate_mag_format(msg)
        self.API_config = get_api_config(api_name=self.model_class)
        address = self.API_config['address']
        if address is None:
            raise ValueError('the api address of ' + self.model_class + " is none.")
        self.chat.append(msg)
        data = {
            "messages": self.chat,
            "temperature": temperature
        }
        result = eval(requests.post(address, data=json.dumps(data)).text)
        self.chat.append(
            {
                "role": "assistant",
                "content": result
            }
        )
        return result, None


class GLM3Agent(LLMAgent):
    def __init__(self, model_category: str):
        super().__init__(model_category)
        if model_category in self.GLM3_LIST:
            self.model_class = 'GLM3'
            self.model_category = model_category
        else:
            raise AttributeError('wrong category: ' + model_category)

    def sse_invoke(self, msg: dict, temperature=float(0), **model_args) -> tuple:
        validate_mag_format(msg)
        self.API_config = get_api_config(api_name=self.model_class)
        address = self.API_config['address']
        if address is None:
            raise ValueError('the api address of ' + self.model_class + " is none.")
        prompt = msg['content']
        history = []
        data = {
            "prompt": prompt,
            "history": history,
            "temperature": temperature
        }
        return eval(requests.post(address, data=json.dumps(data)).text), None


class GLM3Agent_chat(LLMAgent):
    def __init__(self, model_category: str):
        super().__init__(model_category)
        if model_category in self.GLM3_LIST:
            self.model_class = 'GLM3'
            self.model_category = model_category
        else:
            raise AttributeError('wrong category: ' + model_category)
        self.chat = []

    def sse_invoke(self, msg: dict, temperature=float(0), **model_args) -> tuple:
        validate_mag_format(msg)
        self.API_config = get_api_config(api_name=self.model_class)
        address = self.API_config['address']
        if address is None:
            raise ValueError('the api address of ' + self.model_class + " is none.")
        prompt = msg['content']
        data = {
            "prompt": prompt,
            "history": self.chat,
            "temperature": temperature
        }
        self.chat.append(msg)
        result = eval(requests.post(address, data=json.dumps(data)).text)
        self.chat.append(
            {
                "role": "assistant",
                "content": result
            }
        )
        return result, None


class MistralAgent(LLMAgent):
    def __init__(self, model_category: str):
        super().__init__(model_category)
        if model_category in self.Mistral_LIST:
            self.model_class = 'Mistral'
            self.model_category = model_category
        else:
            raise AttributeError('wrong category: ' + model_category)

    def sse_invoke(self, msg: dict, temperature=float(0), **model_args) -> tuple:
        validate_mag_format(msg)
        self.API_config = get_api_config(api_name=self.model_class)
        address = self.API_config['address']
        if address is None:
            raise ValueError('the api address of ' + self.model_class + " is none.")
        data = {
            "messages": [msg],
            "temperature": temperature
        }
        result = eval(requests.post(address, data=json.dumps(data)).text)
        pattern = r'\\n'
        result = re.sub(pattern, '', result)
        pattern = r'\\'
        result = re.sub(pattern, '', result)
        return result, None


class MistralAgent_chat(LLMAgent):
    def __init__(self, model_category: str):
        super().__init__(model_category)
        if model_category in self.Mistral_LIST:
            self.model_class = 'Mistral'
            self.model_category = model_category
        else:
            raise AttributeError('wrong category: ' + model_category)

    def sse_invoke(self, msg: dict, temperature=float(0), **model_args) -> tuple:
        validate_mag_format(msg)
        self.API_config = get_api_config(api_name=self.model_class)
        address = self.API_config['address']
        if address is None:
            raise ValueError('the api address of ' + self.model_class + " is none.")
        self.chat.append(msg)
        data = {
            "messages": self.chat,
            "temperature": temperature
        }
        result = eval(requests.post(address, data=json.dumps(data)).text)
        self.chat.append(
            {
                "role": "assistant",
                "content": result
            }
        )
        return result, None


class GemmaAgent(LLMAgent):
    def __init__(self, model_category: str):
        super().__init__(model_category)
        if model_category in self.Gemma_LIST:
            self.model_class = 'Gemma'
            self.model_category = model_category
            self.chat = []
        else:
            raise AttributeError('wrong category: ' + model_category)

    def sse_invoke(self, msg: dict, temperature=float(0), **model_args) -> tuple:
        validate_mag_format(msg)
        self.API_config = get_api_config(api_name=self.model_class)
        address = self.API_config['address']
        self.chat.append(msg)
        data = {
            "messages": self.chat
        }
        result = eval(requests.post(address, data=json.dumps(data)).text)
        print(result)
        return result, None
