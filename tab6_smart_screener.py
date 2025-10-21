# Tab 6: Smart Stock Screener - Hybrid Implementation
# This file contains the complete Tab 6 code to replace in dashboard_advanced.py

```python
# ========== TAB 6: SMART STOCK SCREENER ==========
with tab6:
    st.header("🎯 Smart Stock Screener")
    st.markdown("*3 chế độ: Lightning (Cache) • Smart Refresh • Deep Scan*")
    
    # Import database
    from database import get_db
    from stock_classifier import StockClassifier
    
    db = get_db()
    classifier = StockClassifier()
    
    # Get cache stats
    cache_stats = db.get_cache_stats()
    
    # Show cache stats at top
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💾 Cached", cache_stats.get('total_cached', 0))
    with col2:
        st.metric("✅ Fresh", cache_stats.get('fresh_24h', 0))
    with col3:
        st.metric("⏰ Outdated", cache_stats.get('outdated_24h', 0))
    with col4:
        coverage = cache_stats.get('coverage_percent', 0)
        st.metric("📊 Coverage", f"{coverage:.0f}%")
    
    if cache_stats.get('last_scan'):
        last_scan_time = datetime.fromisoformat(cache_stats['last_scan'])
        hours_ago = (datetime.now() - last_scan_time).total_seconds() / 3600
        st.caption(f"📅 Last scan: {last_scan_time.strftime('%Y-%m-%d %H:%M')} ({hours_ago:.1f}h ago)")
    
    st.markdown("---")
    
    # Mode selection
    mode = st.radio(
        "**Chọn chế độ Scan:**",
        [
            "⚡ Lightning (0s) - Dùng cache",
            "🔄 Smart Refresh - Cache + update cũ",
            "🚀 Deep Scan - Scan mới hoàn toàn"
        ],
        horizontal=True,
        key="scan_mode",
        help="""
        - ⚡ Lightning: Load từ cache (instant)
        - 🔄 Smart: Dùng cache + refresh stocks > 24h
        - 🚀 Deep: Scan lại hoàn toàn (chậm nhưng fresh nhất)
        """
    )
    
    st.markdown("---")
    
    # Two columns: Settings and Results
    col_settings, col_results = st.columns([1, 2])
    
    with col_settings:
        st.subheader("⚙️ Settings")
        
        # Common settings
        scan_exchange = st.selectbox(
            "Exchange",
            ["All", "HOSE", "HNX"],
            key="scan_exchange"
        )
        
        # Mode-specific settings
        if mode == "⚡ Lightning (0s) - Dùng cache":
            st.success("⚡ Mode: Lightning - Instant load")
            
            cache_age = st.slider(
                "Max cache age (giờ)",
                min_value=1,
                max_value=48,
                value=24,
                help="Chỉ dùng cache nếu < X giờ"
            )
            
            scan_limit = st.slider(
                "Top N stocks",
                min_value=10,
                max_value=100,
                value=20,
                step=10
            )
            
            scan_button_text = "⚡ Load Now (Instant)"
            scan_button_type = "primary"
            
        elif mode == "🔄 Smart Refresh - Cache + update cũ":
            st.info("🔄 Mode: Smart - Cache + refresh outdated")
            
            refresh_count = st.slider(
                "Max stocks to refresh",
                min_value=5,
                max_value=50,
                value=10,
                help="Số lượng stocks cũ sẽ được refresh"
            )
            
            refresh_delay = st.slider(
                "Delay (giây)",
                min_value=6.0,
                max_value=10.0,
                value=8.0,
                step=0.5
            )
            
            estimated_time = refresh_count * (4 + refresh_delay)
            st.caption(f"⏱️ Estimated: ~{estimated_time/60:.1f} phút")
            
            scan_button_text = f"🔄 Smart Scan ({refresh_count} stocks)"
            scan_button_type = "secondary"
            
        else:  # Deep Scan
            st.warning("🚀 Mode: Deep Scan - Full new scan (slowest)")
            
            scan_limit = st.slider(
                "Số lượng stocks",
                min_value=10,
                max_value=100,
                value=20,
                step=10
            )
            
            scan_delay = st.slider(
                "Delay (giây)",
                min_value=6.0,
                max_value=10.0,
                value=8.0,
                step=0.5
            )
            
            estimated_time = scan_limit * (4 + scan_delay)
            st.caption(f"⏱️ Estimated: ~{estimated_time/60:.1f} phút")
            
            scan_button_text = f"🚀 Deep Scan ({scan_limit} stocks)"
            scan_button_type = "primary"
        
        st.markdown("---")
        st.subheader("🔍 Filters")
        
        filter_rating = st.selectbox(
            "Min Rating",
            ["All", "A+", "A", "B", "C", "D"],
            key="filter_rating"
        )
        
        filter_min_score = st.slider(
            "Min Score",
            0.0, 10.0, 5.0, 0.5
        )
        
        st.markdown("---")
        
        # Scan button
        if st.button(scan_button_text, type=scan_button_type, use_container_width=True):
            if mode == "⚡ Lightning (0s) - Dùng cache":
                # LIGHTNING MODE - Load from cache
                with st.spinner("⚡ Loading from cache..."):
                    try:
                        exchange = None if scan_exchange == "All" else scan_exchange
                        min_rating = None if filter_rating == "All" else filter_rating
                        
                        results = db.get_all_cached_classifications(
                            exchange=exchange,
                            max_age_hours=cache_age,
                            min_rating=min_rating,
                            limit=scan_limit
                        )
                        
                        if results:
                            st.session_state['screener_results'] = results
                            st.session_state['screener_mode'] = 'lightning'
                            st.success(f"✅ Loaded {len(results)} stocks in < 1s!")
                            st.rerun()
                        else:
                            st.warning("📦 No cached data found. Try Deep Scan first!")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            
            elif mode == "🔄 Smart Refresh - Cache + update cũ":
                # SMART REFRESH MODE
                with st.spinner(f"🔄 Smart refreshing..."):
                    try:
                        # Get all cached
                        all_cached = db.get_all_cached_classifications(max_age_hours=999)
                        
                        # Separate fresh vs outdated
                        fresh = [s for s in all_cached if s.get('age_hours', 999) < 24]
                        outdated = [s for s in all_cached if s.get('age_hours', 999) >= 24]
                        
                        st.info(f"📦 Fresh: {len(fresh)} | ⏰ Need refresh: {len(outdated)}")
                        
                        # Refresh top N outdated
                        to_refresh = outdated[:refresh_count]
                        
                        refreshed = []
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for i, stock in enumerate(to_refresh):
                            symbol = stock['symbol']
                            status_text.text(f"Refreshing {symbol} ({i+1}/{len(to_refresh)})")
                            
                            # Scan individual stock
                            result = classifier.classify_stock(symbol, use_cache=False, save_cache=True)
                            
                            if not result.get('error'):
                                refreshed.append(result)
                            
                            progress_bar.progress((i + 1) / len(to_refresh))
                            time.sleep(refresh_delay)
                        
                        # Combine fresh + refreshed
                        all_results = fresh + refreshed
                        
                        st.session_state['screener_results'] = all_results[:scan_limit]
                        st.session_state['screener_mode'] = 'smart'
                        st.success(f"✅ Done! {len(fresh)} cached + {len(refreshed)} refreshed")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            
            else:  # Deep Scan
                # DEEP SCAN MODE - Full new scan
                with st.spinner(f"🚀 Deep scanning {scan_limit} stocks..."):
                    try:
                        exchanges = []
                        if scan_exchange == "HOSE":
                            exchanges = ["HOSE"]
                        elif scan_exchange == "HNX":
                            exchanges = ["HNX"]
                        else:
                            exchanges = ["HOSE", "HNX"]
                        
                        # Call API
                        url = f"{API_URL}/classify/market"
                        params = {
                            "exchanges": ",".join(exchanges),
                            "limit": scan_limit,
                            "delay": scan_delay
                        }
                        
                        estimated_time_per_stock = 4 + scan_delay
                        timeout_seconds = int(scan_limit * estimated_time_per_stock * 1.5)
                        
                        st.info(f"⏱️ Timeout: {timeout_seconds}s")
                        
                        response = requests.get(url, params=params, timeout=timeout_seconds)
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            if data.get("success"):
                                st.session_state['screener_results'] = data['stocks']
                                st.session_state['screener_mode'] = 'deep'
                                st.success(f"✅ Scanned {len(data['stocks'])} stocks!")
                                st.rerun()
                            else:
                                st.error(f"❌ {data.get('error')}")
                        else:
                            st.error(f"❌ API Error: {response.status_code}")
                    
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        # Quick actions
        st.markdown("---")
        st.subheader("⚡ Quick Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔝 Top 20", use_container_width=True):
                results = db.get_all_cached_classifications(max_age_hours=24, limit=20)
                if results:
                    st.session_state['screener_results'] = results
                    st.session_state['screener_mode'] = 'quick_top'
                    st.rerun()
                else:
                    st.warning("No cache!")
        
        with col2:
            if st.button("⭐ Watchlist", use_container_width=True):
                watchlist = db.get_watchlist()
                if watchlist:
                    symbols = [w['symbol'] for w in watchlist]
                    results = []
                    for symbol in symbols:
                        cached = db.get_cached_classification(symbol)
                        if cached:
                            results.append(cached['data'])
                    
                    if results:
                        st.session_state['screener_results'] = results
                        st.session_state['screener_mode'] = 'watchlist'
                        st.rerun()
                    else:
                        st.warning("No cached data for watchlist!")
                else:
                    st.warning("Watchlist empty!")
    
    with col_results:
        # Show results if exists
        if 'screener_results' in st.session_state and st.session_state['screener_results']:
            results = st.session_state['screener_results']
            scan_mode = st.session_state.get('screener_mode', 'unknown')
            
            st.subheader(f"📊 Kết quả ({len(results)} stocks)")
            st.caption(f"Mode: {scan_mode}")
            
            # Convert to DataFrame
            df_list = []
            for stock in results:
                df_list.append({
                    'symbol': stock.get('symbol'),
                    'rating': stock.get('overall_rating', {}).get('rating', 'N/A'),
                    'score': stock.get('overall_rating', {}).get('score', 0),
                    'growth': stock.get('classifications', {}).get('growth', {}).get('category', 'N/A'),
                    'risk': stock.get('classifications', {}).get('risk', {}).get('category', 'N/A'),
                    'momentum': stock.get('classifications', {}).get('momentum', {}).get('category', 'N/A'),
                    'recommendation': stock.get('overall_rating', {}).get('recommendation', 'N/A')
                })
            
            df = pd.DataFrame(df_list)
            
            # Apply filters
            if filter_rating != "All":
                df = df[df['rating'] >= filter_rating]
            
            df = df[df['score'] >= filter_min_score]
            
            # Sort by score
            df = df.sort_values('score', ascending=False)
            
            st.write(f"**Filtered: {len(df)} stocks**")
            
            # Display table
            st.dataframe(
                df,
                use_container_width=True,
                height=400
            )
            
            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Download CSV",
                csv,
                "screener_results.csv",
                "text/csv",
                use_container_width=True
            )
            
            # Clear button
            if st.button("🗑️ Clear Results", use_container_width=True):
                del st.session_state['screener_results']
                if 'screener_mode' in st.session_state:
                    del st.session_state['screener_mode']
                st.rerun()
        
        else:
            st.info("👈 Select a mode and click scan button to see results")
            
            # Show guide
            st.markdown("---")
            st.subheader("📖 Hướng dẫn")
            
            st.markdown("""
            **⚡ Lightning Mode:**
            - Load từ cache (< 1 giây)
            - Dùng data đã scan (< 24h)
            - Phù hợp: Xem nhanh, filter, sort
            
            **🔄 Smart Refresh:**
            - Dùng cache + refresh stocks cũ
            - Cân bằng speed/freshness
            - Phù hợp: Update hàng ngày
            
            **🚀 Deep Scan:**
            - Scan mới hoàn toàn
            - Chậm nhưng fresh nhất
            - Phù hợp: First run, critical decisions
            
            **💡 Tips:**
            - Dùng Lightning cho daily screening
            - Dùng Smart Refresh mỗi sáng
            - Dùng Deep Scan 1-2 lần/tuần
            - Setup background scanner cho auto-refresh đêm
            """)
```

