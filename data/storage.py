import os
import json
import asyncio
import aiofiles
from pathlib import Path

class Storage:
    def __init__(self, base_dir=None):
        # 使用项目根目录下的data目录作为默认数据存储位置
        if base_dir:
            self.base_dir = Path(base_dir)
        else:
            # 获取当前文件的绝对路径，然后向上两级到项目根目录
            current_file = Path(__file__).resolve()
            project_root = current_file.parent.parent.parent
            self.base_dir = project_root / "data"
        
        self.base_dir.mkdir(exist_ok=True)
        self.data_files = {
            "users": self.base_dir / "users.json",
            "players": self.base_dir / "players.json",
            "clubs": self.base_dir / "clubs.json",
            "leagues": self.base_dir / "leagues.json",
            "league_levels": self.base_dir / "league_levels.json",
            "national_teams": self.base_dir / "national_teams.json",
            "matches": self.base_dir / "matches.json"
        }
        self.locks = {
            "users": asyncio.Lock(),
            "players": asyncio.Lock(),
            "clubs": asyncio.Lock(),
            "leagues": asyncio.Lock(),
            "league_levels": asyncio.Lock(),
            "national_teams": asyncio.Lock(),
            "matches": asyncio.Lock()
        }
        self._initialize_data_files()
    
    def _initialize_data_files(self):
        for file_path in self.data_files.values():
            if not file_path.exists():
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
    
    async def _read_file(self, file_path):
        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            content = await f.read()
            return json.loads(content)
    
    async def _write_file(self, file_path, data):
        async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(data, ensure_ascii=False, indent=2))
    
    async def get_all(self, collection):
        async with self.locks[collection]:
            data = await self._read_file(self.data_files[collection])
            return data
    
    async def get_by_id(self, collection, item_id):
        async with self.locks[collection]:
            data = await self._read_file(self.data_files[collection])
            for item in data:
                if item["id"] == item_id:
                    return item
            return None
    
    async def create(self, collection, item):
        async with self.locks[collection]:
            data = await self._read_file(self.data_files[collection])
            data.append(item)
            await self._write_file(self.data_files[collection], data)
            return item
    
    async def update(self, collection, item_id, updated_item):
        async with self.locks[collection]:
            data = await self._read_file(self.data_files[collection])
            for i, item in enumerate(data):
                if item["id"] == item_id:
                    data[i] = updated_item
                    await self._write_file(self.data_files[collection], data)
                    return updated_item
            return None
    
    async def delete(self, collection, item_id):
        async with self.locks[collection]:
            data = await self._read_file(self.data_files[collection])
            new_data = [item for item in data if item["id"] != item_id]
            if len(new_data) < len(data):
                await self._write_file(self.data_files[collection], new_data)
                return True
            return False
    
    async def get_by_field(self, collection, field, value):
        async with self.locks[collection]:
            data = await self._read_file(self.data_files[collection])
            return [item for item in data if item.get(field) == value]
    
    async def update_by_field(self, collection, field, value, updated_item):
        async with self.locks[collection]:
            data = await self._read_file(self.data_files[collection])
            updated = False
            for i, item in enumerate(data):
                if item.get(field) == value:
                    data[i] = updated_item
                    updated = True
            if updated:
                await self._write_file(self.data_files[collection], data)
            return updated
    
    async def delete_by_field(self, collection, field, value):
        async with self.locks[collection]:
            data = await self._read_file(self.data_files[collection])
            new_data = [item for item in data if item.get(field) != value]
            if len(new_data) < len(data):
                await self._write_file(self.data_files[collection], new_data)
                return True
            return False
    
    async def clear(self, collection):
        async with self.locks[collection]:
            await self._write_file(self.data_files[collection], [])
    
    async def count(self, collection):
        async with self.locks[collection]:
            data = await self._read_file(self.data_files[collection])
            return len(data)