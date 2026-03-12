import logging
import requests
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime
import io

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
# 🔧 CONFIGURATION - এখানে আপনার টোকেন বসান
# ═══════════════════════════════════════════════════════════════
BOT_TOKEN = "8752407954:AAHIe9NyOLuNFihPTIWF9LJyxkzWkiWVFnI"  # @BotFather থেকে পাওয়া টোকেন
INFO_API_URL = "https://sb-x-hacker-all-info.vercel.app/player-info"
BANNER_API_URL = "https://banner-api-rho.vercel.app/profile"

# ═══════════════════════════════════════════════════════════════
# 👨‍💻 DEVELOPER INFO
# ═══════════════════════════════════════════════════════════════
DEVELOPER_USERNAME = "@SRSabbir"
ADMIN_USERNAME = "@SRSabbir"
BOT_VERSION = "2.0"

# ═══════════════════════════════════════════════════════════════
# 🎨 STYLISH ICONS & DECORATIONS
# ═══════════════════════════════════════════════════════════════
ICONS = {
    'fire': '🔥', 'crown': '👑', 'star': '⭐', 'medal': '🏅',
    'trophy': '🏆', 'game': '🎮', 'id': '🆔', 'user': '👤',
    'globe': '🌍', 'level': '📊', 'exp': '💎', 'rank': '🎯',
    'cs': '🎖️', 'clan': '🏰', 'pet': '🐾', 'social': '💬',
    'like': '❤️', 'badge': '🛡️', 'time': '⏰', 'calendar': '📅',
    'money': '💰', 'shield': '🎭', 'clothes': '👕', 'weapon': '🔫',
    'skin': '🎨', 'signature': '📝', 'language': '🗣️', 'settings': '⚙️',
    'login': '🕐', 'create': '📆', 'version': '🔧', 'pin': '📍',
    'diamond': '💎', 'credit': '💯', 'max': '📈', 'show': '👁️',
    'external': '🔰', 'captain': '👨‍✈️', 'member': '👥', 'capacity': '📊',
    'skill': '⚡', 'choice': '✓', 'arrow': '➤', 'line': '━',
    'double_line': '═', 'bullet': '•', 'sparkle': '✨', 'rocket': '🚀',
    'warning': '⚠️', 'error': '❌', 'success': '✅', 'info': 'ℹ️'
}

def format_timestamp(timestamp):
    """Convert Unix timestamp to readable format"""
    if timestamp:
        try:
            return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        except:
            return "N/A"
    return "N/A"

def get_rank_tier(rank_points):
    """Determine rank tier from ranking points"""
    if rank_points >= 4200:
        return "Grandmaster"
    elif rank_points >= 3600:
        return "Heroic"
    elif rank_points >= 3000:
        return "Diamond"
    elif rank_points >= 2400:
        return "Platinum"
    elif rank_points >= 1800:
        return "Gold"
    elif rank_points >= 1200:
        return "Silver"
    else:
        return "Bronze"

def format_number(num):
    """Format large numbers with commas"""
    if num is None:
        return "N/A"
    try:
        return f"{int(num):,}"
    except:
        return str(num)

def create_header(text):
    """Create stylish header"""
    return f"{ICONS['double_line']*12}\n{text}\n{ICONS['double_line']*12}"

def create_section(title, icon='bullet'):
    """Create stylish section header"""
    return f"\n{ICONS[icon]} <b>{title}</b>\n{ICONS['line']*20}"

# ═══════════════════════════════════════════════════════════════
# 🚀 COMMAND HANDLERS
# ═══════════════════════════════════════════════════════════════

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message"""
    welcome_text = f"""
{ICONS['fire']*3} <b>𝔽ℝ𝔼𝔼 𝔽𝕀ℝ𝔼 𝕌𝕀𝔻 𝕀ℕ𝔽𝕆 𝔹𝕆𝕋</b> {ICONS['fire']*3}

{ICONS['game']} <b>Welcome to the Ultimate Free Fire Bot!</b>

{ICONS['rocket']} <b>Features:</b>
{ICONS['bullet']} Get complete player information
{ICONS['bullet']} Auto banner image display
{ICONS['bullet']} Clan & Pet details
{ICONS['bullet']} Ranking statistics
{ICONS['bullet']} All game assets info

{ICONS['trophy']} <b>Commands:</b>
{ICONS['arrow']} <code>/info &lt;uid&gt;</code> - Get full info + banner
{ICONS['arrow']} <code>/help</code> - Show help menu
{ICONS['arrow']} <code>/admin</code> - Admin information

{ICONS['sparkle']} <b>Example:</b>
<code>/info 9045365047</code>

{ICONS['crown']} <b>Developer:</b> {DEVELOPER_USERNAME}
{ICONS['star']} <b>Version:</b> {BOT_VERSION}
    """
    await update.message.reply_text(welcome_text, parse_mode='HTML')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message with all commands"""
    help_text = f"""
{ICONS['double_line']*15}
{ICONS['info']} <b>ℂ𝕆𝕄𝕄𝔸ℕ𝔻 𝕃𝕀𝕊𝕋</b> {ICONS['info']}
{ICONS['double_line']*15}

{ICONS['game']} <b>User Commands:</b>
{ICONS['line']*25}

{ICONS['fire']} <code>/start</code>
   Start the bot and see welcome message

{ICONS['fire']} <code>/info &lt;uid&gt;</code>
   Get complete player information
   {ICONS['bullet']} Basic Info (ID, Name, Region, Level)
   {ICONS['bullet']} Ranking (BR & CS Rank, Points)
   {ICONS['bullet']} Profile (Avatar, Clothes, Skills)
   {ICONS['bullet']} Clan Information
   {ICONS['bullet']} Pet Details
   {ICONS['bullet']} Social Info
   {ICONS['bullet']} Auto Banner Image

{ICONS['fire']} <code>/help</code>
   Show this help menu

{ICONS['crown']} <b>Admin Commands:</b>
{ICONS['line']*25}

{ICONS['medal']} <code>/admin</code>
   Show admin & developer information

{ICONS['double_line']*15}

{ICONS['warning']} <b>Note:</b>
{ICONS['bullet']} UID must be numeric
{ICONS['bullet']} Banner shows automatically
{ICONS['bullet']} All data is real-time

{ICONS['crown']} <b>Developer:</b> {DEVELOPER_USERNAME}
{ICONS['star']} <b>Admin:</b> {ADMIN_USERNAME}
    """
    await update.message.reply_text(help_text, parse_mode='HTML')

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show admin information"""
    admin_text = f"""
{ICONS['double_line']*15}
{ICONS['crown']} <b>𝔸𝔻𝕄𝕀ℕ 𝕀ℕ𝔽𝕆ℝ𝕄𝔸𝕋𝕀𝕆ℕ</b> {ICONS['crown']}
{ICONS['double_line']*15}

{ICONS['user']} <b>Developer:</b> {DEVELOPER_USERNAME}
{ICONS['medal']} <b>Admin:</b> {ADMIN_USERNAME}
{ICONS['star']} <b>Version:</b> {BOT_VERSION}

{ICONS['trophy']} <b>Bot Features:</b>
{ICONS['line']*25}
{ICONS['success']} Complete player info fetch
{ICONS['success']} Auto banner image display
{ICONS['success']} Clan details with captain info
{ICONS['success']} Pet information
{ICONS['success']} Social statistics
{ICONS['success']} Credit score tracking
{ICONS['success']} Ranking history
{ICONS['success']} All game assets data
{ICONS['success']} Real-time data fetch

{ICONS['rocket']} <b>APIs Used:</b>
{ICONS['line']*25}
{ICONS['bullet']} Info API: Player data
{ICONS['bullet']} Banner API: Profile banner image

{ICONS['double_line']*15}

{ICONS['warning']} <b>Support:</b>
Contact {ADMIN_USERNAME} for help

{ICONS['sparkle']} <b>Thank you for using our bot!</b> {ICONS['sparkle']}
    """
    await update.message.reply_text(admin_text, parse_mode='HTML')

async def get_player_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fetch and display player information + Auto Banner"""
    if not context.args:
        await update.message.reply_text(
            f"{ICONS['error']} <b>ERROR!</b>\n\n"
            f"Please provide a UID.\n\n"
            f"{ICONS['arrow']} <b>Usage:</b> <code>/info &lt;uid&gt;</code>\n"
            f"{ICONS['arrow']} <b>Example:</b> <code>/info 9045365047</code>",
            parse_mode='HTML'
        )
        return

    uid = context.args[0]

    # Validate UID (should be numeric)
    if not uid.isdigit():
        await update.message.reply_text(
            f"{ICONS['error']} <b>ERROR!</b>\n\n"
            f"UID must be numeric (numbers only).",
            parse_mode='HTML'
        )
        return

    # Send "processing" message
    processing_msg = await update.message.reply_text(
        f"{ICONS['rocket']} <b>Fetching player data...</b>\n"
        f"{ICONS['bullet']} UID: <code>{uid}</code>\n"
        f"{ICONS['bullet']} Please wait...",
        parse_mode='HTML'
    )

    try:
        # ═══════════════════════════════════════════════════════════════
        # 📡 CALL INFO API
        # ═══════════════════════════════════════════════════════════════
        info_api_url = f"{INFO_API_URL}?uid={uid}"
        info_response = requests.get(info_api_url, timeout=30)

        if info_response.status_code != 200:
            await processing_msg.edit_text(
                f"{ICONS['error']} <b>ERROR!</b>\n\n"
                f"Failed to fetch data.\n"
                f"Status code: {info_response.status_code}",
                parse_mode='HTML'
            )
            return

        data = info_response.json()

        if not data or 'basicInfo' not in data:
            await processing_msg.edit_text(
                f"{ICONS['error']} <b>ERROR!</b>\n\n"
                f"Player not found or invalid UID.",
                parse_mode='HTML'
            )
            return

        # ═══════════════════════════════════════════════════════════════
        # 📊 EXTRACT ALL DATA
        # ═══════════════════════════════════════════════════════════════
        basic = data.get('basicInfo', {})
        profile = data.get('profileInfo', {})
        clan = data.get('clanBasicInfo', {})
        captain = data.get('captainBasicInfo', {})
        pet = data.get('petInfo', {})
        social = data.get('socialInfo', {})
        credit = data.get('creditScoreInfo', {})
        diamond = data.get('diamondCostRes', {})

        # ═══════════════════════════════════════════════════════════════
        # 🎨 BUILD STYLISH INFO MESSAGE
        # ═══════════════════════════════════════════════════════════════

        # Header
        info_text = f"""
{ICONS['double_line']*18}
{ICONS['game']} <b>ℙ𝕃𝔸𝕐𝔼ℝ 𝕀ℕ𝔽𝕆ℝ𝕄𝔸𝕋𝕀𝕆ℕ</b> {ICONS['game']}
{ICONS['double_line']*18}
"""

        # Basic Information
        info_text += f"""
{ICONS['user']} <b>𝔹𝔸𝕊𝕀ℂ 𝕀ℕ𝔽𝕆</b>
{ICONS['line']*25}
{ICONS['id']} <b>Account ID:</b> <code>{basic.get('accountId', 'N/A')}</code>
{ICONS['crown']} <b>Nickname:</b> <b>{basic.get('nickname', 'N/A')}</b>
{ICONS['globe']} <b>Region:</b> {basic.get('region', 'N/A')}
{ICONS['level']} <b>Level:</b> {basic.get('level', 'N/A')}
{ICONS['exp']} <b>EXP:</b> {format_number(basic.get('exp'))}
{ICONS['medal']} <b>Title ID:</b> {basic.get('title', 'N/A')}
{ICONS['id']} <b>Account Type:</b> {basic.get('accountType', 'N/A')}
"""

        # Ranking Information
        br_tier = get_rank_tier(basic.get('rankingPoints', 0))
        cs_tier = get_rank_tier(basic.get('csRankingPoints', 0))

        info_text += f"""
{ICONS['trophy']} <b>ℝ𝔸ℕ𝕂𝕀ℕ𝔾 𝕀ℕ𝔽𝕆</b>
{ICONS['line']*25}
{ICONS['rank']} <b>BR Rank:</b> {basic.get('rank', 'N/A')} ({br_tier})
{ICONS['star']} <b>BR Points:</b> {format_number(basic.get('rankingPoints'))}
{ICONS['cs']} <b>CS Rank:</b> {basic.get('csRank', 'N/A')} ({cs_tier})
{ICONS['star']} <b>CS Points:</b> {format_number(basic.get('csRankingPoints'))}
{ICONS['max']} <b>Max BR Rank:</b> {basic.get('maxRank', 'N/A')}
{ICONS['max']} <b>Max CS Rank:</b> {basic.get('csMaxRank', 'N/A')}
"""

        # Profile Information
        clothes_list = profile.get('clothes', [])
        equipped_skills = profile.get('equipedSkills', [])

        info_text += f"""
{ICONS['shield']} <b>ℙℝ𝕆𝔽𝕀𝕃𝔼 𝔻𝔼𝕋𝔸𝕀𝕃𝕊</b>
{ICONS['line']*25}
{ICONS['user']} <b>Avatar ID:</b> {profile.get('avatarId', 'N/A')}
{ICONS['skin']} <b>Skin Color:</b> {profile.get('skinColor', 'N/A')}
{ICONS['clothes']} <b>Clothes Count:</b> {len(clothes_list)} items
{ICONS['skill']} <b>Equipped Skills:</b> {len(equipped_skills)} skills
{ICONS['success']} <b>Is Selected:</b> {'Yes' if profile.get('isSelected') else 'No'}
{ICONS['success']} <b>Is Awaken:</b> {'Yes' if profile.get('isSelectedAwaken') else 'No'}
"""

        # Weapon Skins
        weapon_skins = basic.get('weaponSkinShows', [])
        if weapon_skins:
            skins_text = ', '.join(map(str, weapon_skins[:3]))
            if len(weapon_skins) > 3:
                skins_text += f' (+{len(weapon_skins)-3} more)'
            info_text += f"""
{ICONS['weapon']} <b>Weapon Skins:</b> {skins_text}
"""

        # Clan Information
        if clan:
            info_text += f"""
{ICONS['clan']} <b>ℂ𝕃𝔸ℕ 𝕀ℕ𝔽𝕆</b>
{ICONS['line']*25}
{ICONS['crown']} <b>Clan Name:</b> <b>{clan.get('clanName', 'N/A')}</b>
{ICONS['id']} <b>Clan ID:</b> <code>{clan.get('clanId', 'N/A')}</code>
{ICONS['level']} <b>Clan Level:</b> {clan.get('clanLevel', 'N/A')}
{ICONS['member']} <b>Members:</b> {clan.get('memberNum', 'N/A')}/{clan.get('capacity', 'N/A')}
"""

            if captain:
                info_text += f"""
{ICONS['captain']} <b>ℂ𝔸ℙ𝕋𝔸𝕀ℕ 𝕀ℕ𝔽𝕆</b>
{ICONS['line']*25}
{ICONS['crown']} <b>Name:</b> {captain.get('nickname', 'N/A')}
{ICONS['id']} <b>ID:</b> <code>{captain.get('accountId', 'N/A')}</code>
{ICONS['level']} <b>Level:</b> {captain.get('level', 'N/A')}
{ICONS['globe']} <b>Region:</b> {captain.get('region', 'N/A')}
{ICONS['rank']} <b>Rank:</b> {captain.get('rank', 'N/A')}
{ICONS['star']} <b>Points:</b> {format_number(captain.get('rankingPoints'))}
"""

        # Pet Information
        if pet:
            info_text += f"""
{ICONS['pet']} <b>ℙ𝔼𝕋 𝕀ℕ𝔽𝕆</b>
{ICONS['line']*25}
{ICONS['crown']} <b>Pet Name:</b> {pet.get('name', 'N/A')}
{ICONS['id']} <b>Pet ID:</b> {pet.get('id', 'N/A')}
{ICONS['level']} <b>Level:</b> {pet.get('level', 'N/A')}
{ICONS['exp']} <b>EXP:</b> {format_number(pet.get('exp'))}
{ICONS['skin']} <b>Skin ID:</b> {pet.get('skinId', 'N/A')}
{ICONS['skill']} <b>Selected Skill:</b> {pet.get('selectedSkillId', 'N/A')}
{ICONS['success']} <b>Is Selected:</b> {'Yes' if pet.get('isSelected') else 'No'}
"""

        # Social Information
        if social:
            info_text += f"""
{ICONS['social']} <b>𝕊𝕆ℂ𝕀𝔸𝕃 𝕀ℕ𝔽𝕆</b>
{ICONS['line']*25}
{ICONS['signature']} <b>Signature:</b>
<i>"{social.get('signature', 'No signature')}"</i>
{ICONS['language']} <b>Language:</b> {social.get('language', 'N/A').replace('Language_', '')}
{ICONS['show']} <b>Rank Show:</b> {social.get('rankShow', 'N/A').replace('RankShow_', '')}
"""

        # Statistics
        info_text += f"""
{ICONS['star']} <b>𝕊𝕋𝔸𝕋𝕀𝕊𝕋𝕀ℂ𝕊</b>
{ICONS['line']*25}
{ICONS['like']} <b>Likes:</b> {format_number(basic.get('liked'))}
{ICONS['badge']} <b>Badge Count:</b> {basic.get('badgeCnt', 'N/A')}
{ICONS['medal']} <b>Badge ID:</b> {basic.get('badgeId', 'N/A')}
{ICONS['pin']} <b>Pin ID:</b> {basic.get('pinId', 'N/A')}
{ICONS['calendar']} <b>Season ID:</b> {basic.get('seasonId', 'N/A')}
{ICONS['diamond']} <b>Diamond Cost:</b> {diamond.get('diamondCost', 'N/A')}
{ICONS['credit']} <b>Credit Score:</b> {credit.get('creditScore', 'N/A')}/100
{ICONS['medal']} <b>Reward State:</b> {credit.get('rewardState', 'N/A').replace('REWARD_STATE_', '')}
"""

        # External Icon Info
        external_icon = basic.get('externalIconInfo', {})
        if external_icon:
            info_text += f"""
{ICONS['external']} <b>𝔼𝕏𝕋𝔼ℝℕ𝔸𝕃 𝕀ℂ𝕆ℕ</b>
{ICONS['line']*25}
{ICONS['bullet']} <b>Status:</b> {external_icon.get('status', 'N/A').replace('ExternalIconStatus_', '')}
{ICONS['bullet']} <b>Show Type:</b> {external_icon.get('showType', 'N/A').replace('ExternalIconShowType_', '')}
"""

        # Account Preferences
        account_prefers = basic.get('accountPrefers', {})
        if account_prefers:
            br_show = account_prefers.get('brPregameShowChoices', [])
            if br_show:
                info_text += f"""
{ICONS['settings']} <b>𝔸ℂℂ𝕆𝕌ℕ𝕋 ℙℝ𝔼𝔽𝔼ℝ𝔼ℕℂ𝔼𝕊</b>
{ICONS['line']*25}
{ICONS['choice']} <b>BR Pregame Show:</b> {', '.join(map(str, br_show))}
"""

        # Activity Timestamps
        info_text += f"""
{ICONS['time']} <b>𝔸ℂ𝕋𝕀𝕍𝕀𝕋𝕐</b>
{ICONS['line']*25}
{ICONS['login']} <b>Last Login:</b> {format_timestamp(basic.get('lastLoginAt'))}
{ICONS['create']} <b>Account Created:</b> {format_timestamp(basic.get('createAt'))}
{ICONS['version']} <b>Release Version:</b> {basic.get('releaseVersion', 'N/A')}
"""

        # Display Settings
        info_text += f"""
{ICONS['settings']} <b>𝔻𝕀𝕊ℙ𝕃𝔸𝕐 𝕊𝔼𝕋𝕋𝕀ℕ𝔾𝕊</b>
{ICONS['line']*25}
{ICONS['show']} <b>Show BR Rank:</b> {'✅ Yes' if basic.get('showBrRank') else '❌ No'}
{ICONS['show']} <b>Show CS Rank:</b> {'✅ Yes' if basic.get('showCsRank') else '❌ No'}
"""

        # Asset IDs
        banner_id = basic.get('bannerId')
        head_pic = basic.get('headPic')

        if banner_id or head_pic:
            info_text += f"""
{ICONS['shield']} <b>𝔸𝕊𝕊𝔼𝕋 𝕀𝔻𝕊</b>
{ICONS['line']*25}
{ICONS['bullet']} <b>Banner ID:</b> <code>{banner_id}</code>
{ICONS['bullet']} <b>HeadPic ID:</b> <code>{head_pic}</code>
"""

        # Social Highlights
        social_highlights = basic.get('socialHighLightsWithBasicInfo', {})
        if social_highlights:
            info_text += f"""
{ICONS['star']} <b>𝕊𝕆ℂ𝕀𝔸𝕃 ℍ𝕀𝔾ℍ𝕃𝕀𝔾ℍ𝕋𝕊</b>
{ICONS['line']*25}
{ICONS['bullet']} Data available
"""

        # Footer
        info_text += f"""
{ICONS['double_line']*18}
{ICONS['success']} <b>Data fetched successfully!</b>
{ICONS['rocket']} <b>Loading banner image...</b>
{ICONS['crown']} <b>Developer:</b> {DEVELOPER_USERNAME}
{ICONS['double_line']*18}
"""

        # ═══════════════════════════════════════════════════════════════
        # 📤 SEND INFO TEXT
        # ═══════════════════════════════════════════════════════════════
        await processing_msg.delete()
        await update.message.reply_text(info_text, parse_mode='HTML')

        # ═══════════════════════════════════════════════════════════════
        # 🖼️ AUTO BANNER DISPLAY (NO EXTRA COMMAND NEEDED)
        # ═══════════════════════════════════════════════════════════════
        try:
            banner_api_url = f"{BANNER_API_URL}?uid={uid}"
            banner_response = requests.get(banner_api_url, timeout=30)

            if banner_response.status_code == 200 and banner_response.content:
                banner_image = io.BytesIO(banner_response.content)
                banner_image.name = f"banner_{uid}.png"

                await update.message.reply_photo(
                    photo=banner_image,
                    caption=f"""
{ICONS['double_line']*15}
{ICONS['game']} <b>ℙ𝕃𝔸𝕐𝔼ℝ 𝔹𝔸ℕℕ𝔼ℝ</b> {ICONS['game']}
{ICONS['double_line']*15}

{ICONS['id']} <b>UID:</b> <code>{uid}</code>
{ICONS['crown']} <b>Nickname:</b> {basic.get('nickname', 'N/A')}
{ICONS['level']} <b>Level:</b> {basic.get('level', 'N/A')}

{ICONS['crown']} <b>Developer:</b> {DEVELOPER_USERNAME}
{ICONS['double_line']*15}
                    """,
                    parse_mode='HTML'
                )
            else:
                await update.message.reply_text(
                    f"{ICONS['warning']} <b>Banner not available for this UID</b>\n"
                    f"{ICONS['crown']} <b>Developer:</b> {DEVELOPER_USERNAME}",
                    parse_mode='HTML'
                )
        except Exception as banner_error:
            logger.error(f"Banner fetch error: {banner_error}")
            await update.message.reply_text(
                f"{ICONS['warning']} <b>Could not load banner image</b>\n"
                f"{ICONS['crown']} <b>Developer:</b> {DEVELOPER_USERNAME}",
                parse_mode='HTML'
            )

    except requests.exceptions.Timeout:
        await processing_msg.edit_text(
            f"{ICONS['error']} <b>TIMEOUT ERROR!</b>\n\n"
            f"Request timed out. Please try again later.",
            parse_mode='HTML'
        )
    except requests.exceptions.RequestException as e:
        await processing_msg.edit_text(
            f"{ICONS['error']} <b>NETWORK ERROR!</b>\n\n"
            f"<code>{str(e)}</code>",
            parse_mode='HTML'
        )
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        await processing_msg.edit_text(
            f"{ICONS['error']} <b>UNEXPECTED ERROR!</b>\n\n"
            f"<code>{str(e)}</code>",
            parse_mode='HTML'
        )

def main():
    """Start the bot"""
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CommandHandler("info", get_player_info))

    # Run the bot
    print(f"{ICONS['fire']} Bot is starting...")
    print(f"{ICONS['crown']} Developer: {DEVELOPER_USERNAME}")
    print(f"{ICONS['star']} Version: {BOT_VERSION}")
    print(f"{ICONS['success']} Auto Banner Feature: ENABLED")
    print(f"{ICONS['rocket']} All Features Loaded!")

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()