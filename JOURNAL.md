Dev Journal — Donyorbek Ibrohimov 
Phase 0: Python Solidification + Ship v1 (March – June 2026)
Goal: FastAPI backends for AI-powered web tools.
Commit this file every session. 
### Week 1 — Mar 9–15, 2026 
### Monday, Mar 9 
**Topics:** OOP, type hints, @staticmethod, __name__ guard
**What I built:** User class in pure Python — rebuilt from Django’s CustomUser model. Added validate_username() as a
@staticmethod, verify_email() as an instance method.
**What clicked:** @staticmethod vs instance method distinction. If it doesn’t need self, it’s a static.
**Bugs fixed:** __init__ missing closing underscore — object construction was silently broken. isalnum() rejecting underscores.
**Commit:** Phase 0 Day 1: User class - OOP, type hints, staticmethod 
### Tuesday, Mar 10 
**Topics:** 'async/await', 'asyncio.gather'
**What I built:** Two versions of a user fethcher - sync(blocking) and async(non-blocking). Timed both. Sync: ~6s, Async: ~2s.
**What clicked:** 'async def' just enables pausing, 'gather' is what actually runs things in parallel. FastAPI calls gather under the hood - you only write it yourself when one request needs multiple DB calls at once.
**Bugs fixed:** None
**Commit:** 'Phase 0 Day 2: async/await - gather, asyncio.run, sync vs async timing'
### Wednesday, Mar 11 
**Topics:** Decorators
**What I built:** @timer that wraps a function fetch_videos.
**What clicked:** Decorators just expand the function's behaviour without ever changing the original code, they are used for logging, caching, and checking access rights.
**Bugs fixed:** added *args and **kwargs into wrapper so it works on functions with arguements
**Commit:** 'Phase 0 Day 3: Decorators, @timer'
### Friday, Mar 13 
**Topics:** Docstrings
**What I built:** Docstrings for class User's fucnctions and other standalone fucntions.
**What clicked:** Docsstrings explain what the function does and expect, # comments just explain how the code works.
**Bugs fixed:** None
**Commit:** 'Phase 0 Day 4: Docstrings
### Saturday, Mar 14 
**Topics:** Generators, yield, next
**What I built:** A generator to read a large file
**What clicked:** Generators are used to process large files, handle video data - they don't use much memory, because yield just pauses the function and hands back the value, and when you call next() it resumes from where it paused.
**Bugs fixed:** None
**Commit:** 'Phase 0 Day 5: Generators, yield/next'

Week 1 Summary:
Hours: | Commits: | KPIs hit: 
Week 2 — Mar 16–22, 2026 
Monday, Mar 16Topics:
What I built:
What clicked:
Bugs fixed:
Commit: 
Week 2 Summary:
Hours: | Commits: | KPIs hit: