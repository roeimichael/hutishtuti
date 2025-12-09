# Jira Stories - Quick Reference

This document provides a quick-copy format for creating Jira stories from the roadmap.

---

## EPIC 1: Enhanced OCR & Data Capture

### STORY-1.1: Player Position Detection
**Type:** Story
**Priority:** High
**Story Points:** 5
**Labels:** ocr, core, infrastructure

**Description:**
Detect and track all player positions at the table to identify which seats are occupied and track player names/IDs.

**Acceptance Criteria:**
- Calibrate screen coordinates for all player positions (up to 9 players)
- OCR reads player names/IDs from each position
- System tracks which positions are active (seated) vs empty
- System identifies hero (user's) position
- Validate detection accuracy >95% on test screenshots

**Tasks:**
- Extend config.yaml with player_position_locations (9 positions)
- Create ocr_player_detector.py module
- Add player name OCR with tesseract
- Implement empty seat detection (color/pattern matching)
- Add player position calibration to visual calibration tool
- Write unit tests for player detection

**Dependencies:** None

---

### STORY-1.2: Dealer Button Detection
**Type:** Story
**Priority:** High
**Story Points:** 3
**Labels:** ocr, game-state

**Description:**
Detect dealer button location to determine positional play (BTN, SB, BB, UTG, etc.)

**Acceptance Criteria:**
- Calibrate screen coordinates for dealer button icon
- Detect which position has the dealer button
- Calculate relative positions (UTG, MP, CO, BTN, SB, BB)
- Handle button movement between hands
- Validate accuracy >98%

**Tasks:**
- Add dealer_button_locations to config (9 possible positions)
- Implement image pattern matching for dealer button icon
- Create position calculator (UTG+0, UTG+1, etc.)
- Add dealer button to calibration tool
- Add logging for dealer position tracking

**Dependencies:** STORY-1.1

---

### STORY-1.3: Pot Size OCR
**Type:** Story
**Priority:** High
**Story Points:** 3
**Labels:** ocr, numeric

**Description:**
Read and track pot size from screen including main pot and side pots.

**Acceptance Criteria:**
- Calibrate pot size display location
- OCR reads pot amount (handle decimal values)
- Handle different pot displays (main pot, side pots)
- Parse currency symbols and commas correctly
- Validate accuracy >99% on numeric values

**Tasks:**
- Add pot_size_location to config.yaml
- Create numeric OCR function with preprocessing
- Handle currency formatting ($, commas, decimals)
- Add pot size reading to ocr_reader.py
- Add side pot detection logic
- Write tests for numeric parsing

**Dependencies:** None

---

### STORY-1.4: Player Stack Size OCR
**Type:** Story
**Priority:** High
**Story Points:** 5
**Labels:** ocr, numeric, player-data

**Description:**
Read stack sizes for all active players and track changes throughout the hand.

**Acceptance Criteria:**
- Calibrate stack display locations for all 9 positions
- OCR reads numeric stack values
- Track stack changes throughout hand
- Handle abbreviations (1.5K, 2.3M)
- Validate accuracy >95%

**Tasks:**
- Add player_stack_locations to config (9 positions)
- Extend numeric OCR for stack parsing
- Handle abbreviations (K, M suffixes)
- Create stack tracker class
- Add to visual calibration tool
- Write tests for stack tracking

**Dependencies:** STORY-1.1

---

### STORY-1.5: Bet/Action Amount Detection
**Type:** Story
**Priority:** High
**Story Points:** 5
**Labels:** ocr, actions, critical

**Description:**
Detect betting amounts and action types (fold, check, call, bet, raise, all-in) for each player.

**Acceptance Criteria:**
- Calibrate bet amount display locations (9 positions)
- OCR reads bet/raise amounts
- Detect action types (fold, check, call, bet, raise, all-in)
- Track bet amounts per betting round
- Validate accuracy >90%

**Tasks:**
- Add bet_amount_locations to config (9 positions)
- Add action_indicator_locations to config
- Create action detection logic (text + color patterns)
- Implement bet amount tracking per player
- Handle multi-street betting
- Add action detection to calibration tool
- Write action parser tests

**Dependencies:** STORY-1.1, STORY-1.4

---

### STORY-1.6: Blind Level Detection
**Type:** Story
**Priority:** Medium
**Story Points:** 2
**Labels:** ocr, game-info

**Description:**
Detect current small blind and big blind amounts from the table display.

**Acceptance Criteria:**
- Calibrate blind display location
- OCR reads SB/BB amounts
- Track blind level changes
- Validate accuracy >99%

**Tasks:**
- Add blind_level_location to config
- Create blind level parser
- Add blind tracking to game state
- Write blind level tests

**Dependencies:** None

---

## EPIC 2: Game State Management & Event Detection

### STORY-2.1: Hand State Machine
**Type:** Story
**Priority:** High
**Story Points:** 8
**Labels:** core, state-management, architecture

**Description:**
Create comprehensive state machine to track hand progression from preflop through showdown.

**Acceptance Criteria:**
- State machine tracks: preflop → flop → turn → river → showdown
- Detect new hand start
- Detect betting round transitions
- Track active players per street
- Handle hand completion/reset

**Tasks:**
- Create hand_state_machine.py module
- Define state enum (WAITING, PREFLOP, FLOP, TURN, RIVER, SHOWDOWN)
- Implement state transition logic
- Add new hand detection (card reset, pot reset)
- Add betting round completion detection
- Integrate with existing Game class
- Write state machine unit tests

**Dependencies:** EPIC-1 stories

---

### STORY-2.2: Action Sequence Tracking
**Type:** Story
**Priority:** High
**Story Points:** 5
**Labels:** data-collection, actions

**Description:**
Track all player actions in chronological sequence during a hand with timestamps.

**Acceptance Criteria:**
- Record action order with timestamps
- Track action type and amount for each player
- Maintain action history per betting round
- Handle out-of-turn actions gracefully
- Export action sequence in chronological order

**Tasks:**
- Create ActionTracker class
- Add timestamp to action records
- Implement action queue per betting round
- Add action validation logic
- Integrate with hand state machine
- Write action tracking tests

**Dependencies:** STORY-2.1, STORY-1.5

---

### STORY-2.3: Continuous Screenshot & Event Loop
**Type:** Story
**Priority:** High
**Story Points:** 8
**Labels:** core, performance, monitoring

**Description:**
Implement continuous monitoring of poker table with efficient change detection.

**Acceptance Criteria:**
- Take screenshots at configurable intervals (e.g., every 500ms)
- Detect changes in game state automatically
- Trigger appropriate OCR based on detected changes
- Handle performance efficiently (don't block)
- Add start/stop controls

**Tasks:**
- Create game_monitor.py with continuous loop
- Implement async screenshot capture
- Add change detection (compare screenshots)
- Create event dispatcher for game state changes
- Add configurable polling interval
- Implement resource cleanup
- Add threading/async support
- Write integration tests

**Dependencies:** STORY-2.1

---

### STORY-2.4: Hand Completion Detection
**Type:** Story
**Priority:** High
**Story Points:** 3
**Labels:** game-state, data-collection

**Description:**
Detect when a hand ends (showdown or all-fold) and prepare for next hand.

**Acceptance Criteria:**
- Detect showdown or all-fold scenarios
- Capture final pot winner(s)
- Reset game state for next hand
- Trigger data export
- Handle multi-way pots

**Tasks:**
- Create hand completion detector
- Add winner detection logic
- Implement state reset functionality
- Add hand summary generation
- Write completion detection tests

**Dependencies:** STORY-2.1, STORY-2.2

---

## EPIC 3: Data Storage & CSV Export

### STORY-3.1: Data Model Design
**Type:** Story
**Priority:** High
**Story Points:** 3
**Labels:** data, architecture, design

**Description:**
Design comprehensive data schema for poker hand history with all relevant fields.

**Acceptance Criteria:**
- Define CSV schema for hand history
- Define schema for player actions
- Define schema for game metadata
- Document all fields and data types
- Review and approve with team

**Tasks:**
- Create data model documentation
- Define HandHistory dataclass
- Define PlayerAction dataclass
- Define GameMetadata dataclass
- Create schema validation rules
- Add example CSV files

**Deliverables:**
- HAND_HISTORY.csv schema
- PLAYER_ACTIONS.csv schema
- GAME_METADATA.csv schema
- Data dictionary document

**Dependencies:** EPIC-2

---

### STORY-3.2: CSV Writer Module
**Type:** Story
**Priority:** High
**Story Points:** 5
**Labels:** data, export

**Description:**
Implement CSV export functionality with validation and safe concurrent writes.

**Acceptance Criteria:**
- Export hand history to CSV
- Export player actions to CSV
- Export game metadata to CSV
- Handle file creation and appending
- Add data validation before export
- Handle concurrent writes safely

**Tasks:**
- Create csv_exporter.py module
- Implement HandHistoryWriter class
- Implement PlayerActionWriter class
- Add CSV validation logic
- Add file locking for concurrent access
- Configure export directory
- Write CSV export tests

**Dependencies:** STORY-3.1

---

### STORY-3.3: Real-time Data Logging
**Type:** Story
**Priority:** High
**Story Points:** 3
**Labels:** data, real-time

**Description:**
Log data in real-time as hand progresses with proper error handling.

**Acceptance Criteria:**
- Append actions to CSV as they occur
- Finalize hand record when hand completes
- Handle interrupted hands gracefully
- Add data integrity checks
- Validate CSV format

**Tasks:**
- Integrate CSV writer with game monitor
- Add action logging hooks
- Add hand completion hooks
- Implement transaction-like hand recording
- Add error recovery for incomplete hands
- Write integration tests

**Dependencies:** STORY-3.2, STORY-2.4

---

### STORY-3.4: Data Export Configuration
**Type:** Story
**Priority:** Medium
**Story Points:** 2
**Labels:** config, ui

**Description:**
Add UI controls and configuration for data export settings.

**Acceptance Criteria:**
- Add export settings to config.yaml
- Add export directory selection
- Add enable/disable toggle for logging
- Add file rotation settings (max file size)
- Display export status in GUI

**Tasks:**
- Add export config section to config.yaml
- Create export settings UI panel
- Implement file rotation logic
- Add export status indicator
- Write config tests

**Dependencies:** STORY-3.2

---

## EPIC 4: Data Preprocessing & Feature Engineering

### STORY-4.1: Data Cleaning Pipeline
**Type:** Story
**Priority:** Medium
**Story Points:** 5
**Labels:** data, ml-prep

**Description:**
Clean and validate collected CSV data before training.

**Acceptance Criteria:**
- Remove incomplete/invalid hands
- Validate data integrity
- Handle missing values
- Detect and flag anomalies
- Generate data quality report

**Tasks:**
- Create data_cleaner.py module
- Implement validation rules
- Add missing value imputation strategies
- Create anomaly detection logic
- Generate data quality metrics
- Write cleaning pipeline tests

**Dependencies:** EPIC-3

---

### STORY-4.2: Feature Engineering
**Type:** Story
**Priority:** High
**Story Points:** 8
**Labels:** ml, features, critical

**Description:**
Create neural network features from raw game data including pot odds, SPR, position features, etc.

**Acceptance Criteria:**
- Calculate pot odds for each decision
- Compute stack-to-pot ratios (SPR)
- Create position features (early/mid/late)
- Calculate aggression frequencies
- Generate player profiling features
- Encode categorical variables
- Normalize numeric features

**Tasks:**
- Create feature_engineering.py module
- Implement pot odds calculator
- Implement SPR calculator
- Create position encoder
- Add player statistics aggregator
- Implement one-hot encoding for categories
- Add feature scaling/normalization
- Document all features
- Write feature generation tests

**Dependencies:** STORY-4.1

---

### STORY-4.3: Train/Validation/Test Split
**Type:** Story
**Priority:** Medium
**Story Points:** 2
**Labels:** ml, data

**Description:**
Split dataset for proper ML evaluation without data leakage.

**Acceptance Criteria:**
- Implement time-based split (no data leakage)
- Create train (70%), validation (15%), test (15%) sets
- Ensure session-level splits (no hand leakage)
- Save split indices for reproducibility
- Validate split quality

**Tasks:**
- Create data_splitter.py module
- Implement time-series split logic
- Add session grouping
- Save split metadata
- Write split validation tests

**Dependencies:** STORY-4.2

---

### STORY-4.4: Data Augmentation
**Type:** Story
**Priority:** Medium
**Story Points:** 5
**Labels:** ml, data

**Description:**
Augment training data to improve model generalization and handle class imbalance.

**Acceptance Criteria:**
- Implement position rotation augmentation
- Add suit isomorphism (card suit swapping)
- Balance dataset (handle class imbalance)
- Configure augmentation pipeline
- Validate augmented data quality

**Tasks:**
- Create data_augmentation.py module
- Implement position rotation
- Implement suit isomorphism
- Add SMOTE for imbalanced classes
- Create augmentation config
- Write augmentation tests

**Dependencies:** STORY-4.2

---

## EPIC 5: Neural Network Model Development

### STORY-5.1: Model Architecture Design
**Type:** Story
**Priority:** Medium
**Story Points:** 5
**Labels:** ml, research, architecture

**Description:**
Design neural network architecture for poker action recommendation.

**Acceptance Criteria:**
- Research poker AI architectures
- Design network topology (layers, neurons, activations)
- Choose loss function and optimizer
- Define input/output format
- Document architecture decisions

**Tasks:**
- Research existing poker AI models
- Design DNN architecture (candidate: 3-5 dense layers)
- Define multi-class output (fold, check, call, bet, raise)
- Choose framework (PyTorch vs TensorFlow)
- Create architecture diagram
- Write architecture documentation

**Dependencies:** STORY-4.2

---

### STORY-5.2: Model Implementation
**Type:** Story
**Priority:** Medium
**Story Points:** 5
**Labels:** ml, implementation

**Description:**
Implement neural network in chosen framework with training infrastructure.

**Acceptance Criteria:**
- Implement model class
- Add forward pass logic
- Add training loop
- Add validation loop
- Implement checkpointing
- Add TensorBoard logging

**Tasks:**
- Create poker_nn_model.py module
- Implement PokerNetwork class
- Add training script
- Add validation metrics
- Implement model checkpointing
- Add TensorBoard integration
- Write model tests

**Dependencies:** STORY-5.1

---

### STORY-5.3: Training Pipeline
**Type:** Story
**Priority:** Medium
**Story Points:** 5
**Labels:** ml, training

**Description:**
Create end-to-end training pipeline from data loading to model saving.

**Acceptance Criteria:**
- Load preprocessed data
- Create data loaders/batching
- Train model with hyperparameters
- Track training metrics
- Save trained model
- Generate training report

**Tasks:**
- Create train.py script
- Implement data loading pipeline
- Add batch generation logic
- Implement training loop with logging
- Add early stopping
- Create model serialization
- Write training documentation

**Dependencies:** STORY-5.2, STORY-4.3

---

### STORY-5.4: Model Evaluation
**Type:** Story
**Priority:** Medium
**Story Points:** 3
**Labels:** ml, evaluation

**Description:**
Evaluate model performance on test set and compare against baseline.

**Acceptance Criteria:**
- Calculate accuracy, precision, recall, F1
- Generate confusion matrix
- Analyze per-action performance
- Compare against baseline (GTO charts)
- Create evaluation report

**Tasks:**
- Create evaluate_model.py script
- Implement evaluation metrics
- Generate confusion matrix
- Create performance visualizations
- Write evaluation report
- Compare with baseline strategy

**Dependencies:** STORY-5.3

---

### STORY-5.5: Hyperparameter Tuning
**Type:** Story
**Priority:** Low
**Story Points:** 5
**Labels:** ml, optimization

**Description:**
Optimize model hyperparameters to improve performance.

**Acceptance Criteria:**
- Define hyperparameter search space
- Implement grid/random search
- Track experiment results
- Select best configuration
- Document tuning process

**Tasks:**
- Set up hyperparameter search framework
- Define search space (learning rate, layers, dropout, etc.)
- Run tuning experiments
- Log results with MLflow or W&B
- Select and validate best model
- Write tuning report

**Dependencies:** STORY-5.3

---

## EPIC 6: Model Integration & Real-time Inference

### STORY-6.1: Model Inference Module
**Type:** Story
**Priority:** Medium
**Story Points:** 3
**Labels:** ml, inference, integration

**Description:**
Create module for real-time model predictions during live play.

**Acceptance Criteria:**
- Load trained model
- Prepare game state features
- Get action predictions
- Return confidence scores
- Handle errors gracefully

**Tasks:**
- Create model_inference.py module
- Implement model loader
- Add feature preparation function
- Implement prediction function
- Add confidence threshold logic
- Write inference tests

**Dependencies:** STORY-5.3

---

### STORY-6.2: GUI Integration
**Type:** Story
**Priority:** Medium
**Story Points:** 5
**Labels:** ui, ml, integration

**Description:**
Display AI recommendations in GUI with confidence scores and alternatives.

**Acceptance Criteria:**
- Add AI recommendation panel to GUI
- Show recommended action
- Display confidence percentage
- Show alternative actions with probabilities
- Add enable/disable toggle
- Update in real-time during game

**Tasks:**
- Extend run_game_gui.py with AI panel
- Create recommendation display widget
- Add confidence bar visualization
- Implement real-time inference calls
- Add AI toggle setting
- Write GUI integration tests

**Dependencies:** STORY-6.1

---

### STORY-6.3: Performance Optimization
**Type:** Story
**Priority:** Medium
**Story Points:** 3
**Labels:** performance, optimization

**Description:**
Optimize inference speed for real-time use without UI blocking.

**Acceptance Criteria:**
- Inference completes in <100ms
- No UI blocking during inference
- Efficient model loading (cache)
- Profile and optimize bottlenecks
- Measure and document performance

**Tasks:**
- Profile inference pipeline
- Optimize feature preparation
- Add model caching
- Implement async inference
- Run performance benchmarks
- Write optimization report

**Dependencies:** STORY-6.1

---

### STORY-6.4: Action Explanation Module
**Type:** Story
**Priority:** Low
**Story Points:** 5
**Labels:** ml, explainability, ui

**Description:**
Provide explanations for AI recommendations using explainability techniques.

**Acceptance Criteria:**
- Explain why action was recommended
- Show key contributing features
- Display relevant statistics
- Add explainability UI
- Support multiple explanation types

**Tasks:**
- Implement SHAP or LIME explainability
- Create explanation generator
- Add feature importance display
- Create explanation UI panel
- Write explanation tests

**Dependencies:** STORY-6.1

---

## EPIC 7: Testing, Documentation & Deployment

### STORY-7.1: Unit Test Coverage
**Type:** Story
**Priority:** High
**Story Points:** 8
**Labels:** testing, quality

**Description:**
Achieve >80% unit test coverage across the codebase.

**Acceptance Criteria:**
- Write unit tests for all core modules
- Achieve >80% code coverage
- Add continuous integration (CI)
- All tests pass consistently
- Generate coverage report

**Tasks:**
- Write tests for OCR modules
- Write tests for game state logic
- Write tests for CSV export
- Write tests for feature engineering
- Write tests for model inference
- Set up pytest-cov
- Configure GitHub Actions CI
- Generate coverage badge

**Dependencies:** All prior stories

---

### STORY-7.2: Integration Tests
**Type:** Story
**Priority:** High
**Story Points:** 5
**Labels:** testing, quality

**Description:**
Test end-to-end workflows to ensure system works as a whole.

**Acceptance Criteria:**
- Test complete hand capture workflow
- Test CSV export workflow
- Test model inference workflow
- Test GUI interactions
- All integration tests pass

**Tasks:**
- Create integration test suite
- Write end-to-end capture tests
- Write end-to-end inference tests
- Create test fixtures (screenshots)
- Set up test database/CSV
- Run integration tests in CI

**Dependencies:** EPIC-6

---

### STORY-7.3: User Documentation
**Type:** Story
**Priority:** Medium
**Story Points:** 5
**Labels:** documentation

**Description:**
Create comprehensive user documentation for all features.

**Acceptance Criteria:**
- Update README with new features
- Create setup guide
- Create calibration guide
- Create data collection guide
- Create AI training guide
- Add troubleshooting section

**Tasks:**
- Update README.md
- Create SETUP_GUIDE.md
- Create DATA_COLLECTION_GUIDE.md
- Create AI_TRAINING_GUIDE.md
- Create TROUBLESHOOTING.md
- Add screenshots/diagrams
- Review documentation

**Dependencies:** EPIC-6

---

### STORY-7.4: Code Quality Improvements
**Type:** Story
**Priority:** High
**Story Points:** 5
**Labels:** refactoring, quality, technical-debt

**Description:**
Implement code quality improvements from audit including logging, type hints, and dead code removal.

**Acceptance Criteria:**
- Replace all print() with logging
- Remove dead code (card_display.py, etc.)
- Add type hints to all functions
- Fix code duplication
- Refactor long methods
- Pass linting checks

**Tasks:**
- Add logging module configuration
- Replace print statements with logging
- Remove unused files
- Add type hints throughout
- Refactor duplicate code
- Break up long methods
- Run pylint/flake8
- Fix all linting errors

**Dependencies:** None (can start immediately)

---

### STORY-7.5: Deployment Package
**Type:** Story
**Priority:** Low
**Story Points:** 3
**Labels:** deployment, ops

**Description:**
Create distributable package for easy installation.

**Acceptance Criteria:**
- Create setup.py
- Add requirements.txt with all deps
- Create Docker container (optional)
- Add installation script
- Test installation on clean system

**Tasks:**
- Create setup.py
- Update requirements.txt
- Create Dockerfile
- Write install.sh script
- Test on Windows/Mac/Linux
- Write deployment documentation

**Dependencies:** STORY-7.3

---

## COPY-PASTE TEMPLATES

### Creating an Epic in Jira:
```
Name: EPIC-X: [Epic Name]
Description: [From roadmap]
Start Date: [TBD]
End Date: [TBD]
Labels: [From roadmap]
```

### Creating a Story in Jira:
```
Type: Story
Epic Link: EPIC-X
Summary: STORY-X.Y: [Story Name]
Priority: [High/Medium/Low]
Story Points: [Number]
Labels: [Comma separated]

Description:
[Copy description from above]

Acceptance Criteria:
[Copy checklist items as checkbox format]

Tasks:
[Copy task list as subtasks in Jira]

Dependencies:
[Add story links]
```

---

**Instructions:**
1. Create Epics 1-7 first
2. Create all stories within each Epic
3. Link dependencies between stories
4. Assign story points
5. Add labels for filtering
6. Start Sprint 1 planning with recommended stories
